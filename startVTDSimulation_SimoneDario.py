import subprocess, logging, os, time, datetime, shutil, random, string, sys, glob
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
import SelectFromCSV

from src.utils import DRIVER_PARAMS_LABEL_TO_NAME, read_configurations, configure_loggers, make_output_folders, copy_files
##from src.utils import FMU_DEFAULT_PATH, generate_fmu_mapping_car, fmu_mapping_car_path
from src.adams import shrink_results
from src.adams import TooManyResultsError, generate_post_processing_files

###START PROGRAM###

def scriptVTD ():
    launching_dir = os.getcwd() #setta la variabile launching_dir alla current working directory

    try: #eccezione che mi manda un messaggio nel caso non venga trovata una configurazione del driver/scenario
        configuration, sim_configuration, driver_configuration = read_configurations(['config.json', 'sim_config.json', 'driver_config.json'])
    except FileNotFoundError as e:
        print('Missing configuration file.\n{error}'.format(error=str(e)))
        sys.exit(-1)


    app_start = datetime.datetime.fromtimestamp(time.time()) #registra il modo in cui uno script viene avviato    

    ## CREO LE CARTELLE DI OUTPUT CON LA FUNZIONE MAKE OUTPUT FOLDERS
    #crea una cartella per gli output ricevendo in input configuration che e la var. definita sopra
    log_folder, output_folder = make_output_folders([configuration['logFolder'], configuration['outputFolder']], launching_dir, app_start)

    #configurazione dei logger 
    configure_loggers(log_folder, app_start)
    logger = logging.getLogger('root')

    #togliere i file che si creano dopo la simulazione all'interno della cartella tmp, sono i file delle finestre colorate che si aprono
    for filename in glob.glob(os.path.join('/tmp', 'taskRec_*.txt')):
        if os.path.exists(filename):
            logger.info('Clean: deleting '+ filename)
            os.remove(filename)            
        
    #copia i seguenti file nella cartella output_folders, per avere in ogni cartella di output anche la configurazione corrispondente
    copy_files(['sim_config.json', 'driver_config.json'], output_folder)

    os.chdir(os.environ['VTD_ROOT'])

    seconds_between_processes = int(configuration['secondsBetweenProcesses']) #se guardo all'interno di conf.json vedo che i secondi da aspettare sono 5

    from src.scp import SCPCommand, launch_scp #importa la classe SCPCommand e il metodo launch_scp

    #open apre/crea i 3 file in scrittura all'interno della cartella log e a sua volta all'interno di un'altra cartella che indica la data,
    #os.path.join crea il percorso mettendo assieme il nome della cartella specificata da log_folder e la stringa. il tutto viene identificato con il nome dopo as
    with open(os.path.join(log_folder, 'vtdStartViaSCP_start.log'), 'w+') as vtd_out,\
        open(os.path.join(log_folder, 'scp.log'), 'w+') as scp_out,\
        open(os.path.join(log_folder, 'scp_monitor.log'), 'w+') as scp_monitor_out,\
        open(os.path.join(log_folder, 'rdbSniffer.log'), 'w+') as rdb_out: 
        
        for sim_name, sim_params in sim_configuration.items(): #nome della simulazione e i suoi parametri

            scenario_file, driver_config_name = sim_params['scenarioFile'], sim_params['driverConfigName'] if 'driverConfigName' in sim_params.keys() else None #assegno alle 2 variabili i vari parametri di scenarioFile e driverConfigName che sono presenti in sim_config.json. Se la chiave esiste si assegna il valore, altrimenti no
            
            ##fmu_path = sim_params['fmuPath'] if 'fmuPath' in sim_params.keys() else FMU_DEFAULT_PATH 

            ##logger.info('Generating fmu-mapping-car.xml with fmu -> {fmu_path}'.format(fmu_path=fmu_path))
            ##logger.debug('fmu-mapping-car.xml path -> {fmu_mapping_car_path}'.format(fmu_mapping_car_path=fmu_mapping_car_path))
            ##generate_fmu_mapping_car(fmu_path)

            logger.info('Starting ' + sim_name) #inizio la simulazione
            logger.info('Killing previous instances...') #chiudo se ci sono altre simulazioni in corso, uso vtdStop.sh
            with subprocess.Popen(os.path.join(os.environ['VTD_ROOT'], 'bin', 'vtdStop.sh'), stdout=subprocess.PIPE, shell=True) as p: #reindirizzo lo standard output in una pipe cosi posso catturarlo
                logger.info('{p_out}'.format(p_out=p.stdout.read().decode('utf-8')))
            time.sleep(seconds_between_processes)

            logger.info('Opening VTD') #apro VTD 
            vtd_launch_cmd =[os.path.join(os.environ['VTD_ROOT'], 'bin', 'vtdStart.sh'), '--project=' + os.environ['SM_SETUP'], '--autoConfig'] #creo il comando per lanciare VTD, come quando lo faccio dalla shell, ovvero digito il percorso, poi il programma, e ci aggiungo anche gia il setup con il quale voglio lanciarlo
            logger.debug('Launch command -> ' + ' '.join(vtd_launch_cmd)) #lancio VTD con autoConfig/Standard.noIG  --setup=Standard.noIG
            print(vtd_launch_cmd) #['/opt/MSC.Software/VTD.2023.2/bin/vtdStart.sh', '--project=SD_Project', '--autoConfig']
            vtd_process = subprocess.Popen(vtd_launch_cmd, stdout=vtd_out, stderr=vtd_out) #reindirizzamento standard output e standard error
            logger.debug('VTD instance -> ' + str(vtd_process.pid)) #vtd_process l'ho definita sopra, con .pid prendo il PID del processo
            time.sleep(seconds_between_processes)

            logger.debug('Launching SCP Monitor -> ' + ' '.join([os.path.join(os.environ['VTD_SCP_GENERATOR_EXE']), '-m'])) #genero SCP monitor
            subprocess.Popen([os.path.join(os.environ['VTD_SCP_GENERATOR_EXE']), '-m'], stdout=scp_monitor_out, stderr=scp_monitor_out) #reindirizzo stanrd output e standard error 
            time.sleep(seconds_between_processes)

            #classe SCP command e eseguo il metodo cmd che vuole determinati parametri (vedi commandGenerator.py)
            logger.info('Loading Scenario ' + scenario_file) #carico lo scenario
            command = SCPCommand().sync_with_sim().no_wait().cmd('Display', command=SCPCommand().self_closed_tag('Database', {'enable': 'true', 'streetLamps': 'true'}))\
                .no_wait().cmd('Display', command=SCPCommand().self_closed_tag('Database', {'enable': 'true', 'headlights': 'false'}))\
                .no_wait().sim_ctrl(SCPCommand().self_closed_tag('LoadScenario', {'filename': scenario_file}))\
                .no_wait().cmd('Traffic',attributes={},command=SCPCommand().set_parameters([{'driverType': 'DefaultDriver'}]))\
                .no_wait().sensor('Sensor_MM', 'video', {
                    'Load': {'lib': 'libModulePerfectSensor.so',
                            'path': '/opt/MSC.Software/VTD.2023.2/Data/Projects/SD_Project/Plugins/ModuleManager'},
                            #'path': '/home/vtd/VIRES/VTD.2022.3/Data/Projects/../Distros/Current/Plugins/ModuleManager'},
                    'Player': {'name': 'Ego'},
                    'Frustum': {'bottom': '6.000000',
                                'far': '40.00000',
                                'left': '15.000000',
                                'near':"1.000000",
                                'right':"15.000000",
                                'top':"6.000000"},
                    'Position': {'dhDeg':"0.000000",
                                'dpDeg':"0.000000",
                                'drDeg':"0.000000",
                                'dx':"0.000000",
                                'dy':"0.000000",
                                'dz':"0.000000"},
                    'Origin': {'type':'usk'},
                    'Cull': {'enable':"true",
                            'maxObjects':"10"},
                    'Port': {'name':"RDBout",
                            'number':"48185",
                            'sendEgo':"true",
                            'type':"TCP"},
                    'Filter':{'objectType':"all"},
                    'Debug':{'camera':"false",
                            'culling':"false",
                            'detection':"false",
                            'dimensions':"false",
                            'enable':"false",
                            'packages':"false",
                            'position':"false",
                            'road':"false"}
                })
            launch_scp(command, scp_out, scp_out, seconds_between_processes)

            logger.info('Apply configuration')
            command = SCPCommand()\
                .sync_with_sim()\
                .no_wait().sim_ctrl(SCPCommand().tag('Apply'))
            launch_scp(command, scp_out, scp_out, seconds_between_processes)
            
            #a questo punto lo scenario e` pronto

        
            logger.info('Start VTD simulation')
            sim_start_time = datetime.datetime.now() #prendo il tempo di inizio simulazione 

            command = SCPCommand()\
                .sync_with_sim()\
                .no_wait().sim_ctrl(SCPCommand().self_closed_tag('Init', {'mode': 'operation'}))\
                .wait().append_str('"<SimCtrl> <InitDone place="checkInitConfirmation"/> </SimCtrl>"')
            if driver_config_name and driver_config_name in driver_configuration.keys(): #definisco il driver
                command = command.no_wait().cmd('Player', {'name': 'Ego'}, SCPCommand().self_closed_tag('DriverBehaviorNormalized', {DRIVER_PARAMS_LABEL_TO_NAME[key]: value for key, value in driver_configuration[driver_config_name].items() if DRIVER_PARAMS_LABEL_TO_NAME[key] != ''}))
            command = command.no_wait().sim_ctrl(SCPCommand().self_closed_tag('Start')) #lancio la simulazione 
            
            launch_scp(command, scp_out, scp_out, 0)

            sim_output_folder = os.path.join(output_folder, scenario_file[:-4], driver_config_name if 'driverConfigName' in sim_params.keys() else ''.join(random.choice(string.ascii_letters) for _ in range(6)))
            logger.info('Creating output folder -> ' + str(sim_output_folder))
            sim_output_debug_folder = os.path.join(sim_output_folder, '.debug')
            os.makedirs(sim_output_debug_folder)

            rdbSniffer_output_file = os.path.join(sim_output_debug_folder, 'Dati_rdbSniffer.csv')
            logger.info('Creating RDBSniffer output file -> ' + str(rdbSniffer_output_file))

            logger.info('Opening rdbSniffer...') # + ' -c tcp -d -pkg 5 -csv prova'
            rdbSniffer_launch_cmd = [os.path.join(os.environ['RDB_ROOT'], 'rdbSniffer'),'-c', 'tcp', '-d', '-pkg', '5', '-csv', rdbSniffer_output_file] 
            logger.debug('Launch command rdb -> ' + ' '.join(rdbSniffer_launch_cmd))
            rdbSniffer_process = subprocess.Popen(rdbSniffer_launch_cmd, stdout=rdb_out, stderr=rdb_out) #reindirizzamento standard output e standard error
            logger.debug('RDB instance -> ' + str(rdbSniffer_process.pid)) #vtd_process l'ho definita sopra, con .pid prendo il PID del processo
            time.sleep(seconds_between_processes)
            sim_completed = False
            
            try: #<SimCtrl><DelayedStop value="true"/></SimCtrl>
                logger.info('Waiting for stop trigger...') #aspetto che si attivi un trigger e mi arrivi un messaggio, cattura il trigger che fa fermare la macchina
                command = SCPCommand()\
                    .wait().sim_ctrl(SCPCommand().self_closed_tag('DelayedStop', {'value': 'true'}))\
                    .wait(1).cmd_enveloping_self_closed_tags('Symbol', {'name': 'exp101'},{
                        'Text': {'data': "Got trigger", 'colorRGB':"0xffff00", 'size':"50.0"},
                        'PosScreen': {'x':"0.01", 'y':"0.05"}
                    })
                launch_scp(command, out_handler=scp_out, error_handler=scp_out, timeout_min=int(configuration['simulationTimeoutMinutes']))
                logger.info('Scenario terminated')
                sim_completed = True #simulazione completata
            except subprocess.TimeoutExpired as e: #qui uso le eccezioni per catturare errori nel caso ci fossero
                logger.error('Simulation {sim_name} has timed out!'.format(sim_name=sim_name))
                logger.debug(str(e))
            finally:
                logger.info('Killing VTD...')
                with subprocess.Popen(os.path.join(os.environ['VTD_ROOT'], 'bin', 'vtdStop.sh'), stdout=subprocess.PIPE, shell=True) as p:
                    logger.info('{p_out}'.format(p_out=p.stdout.read().decode('utf-8')))
                logger.info('Killing RDBSniffer...')
                try:
                    # Termina il processo utilizzando il suo PID
                    os.kill(rdbSniffer_process.pid, 9)  # Il segnale 9 è il segnale KILL, che forza la terminazione del processo
                    print(f"Processo con PID {rdbSniffer_process.pid} terminato con successo.")
                except ProcessLookupError:
                    print(f"Processo con PID {rdbSniffer_process.pid} non trovato.")
                except Exception as e:
                    print(f"Errore durante la terminazione del processo: {str(e)}")

                duration = datetime.datetime.now() - sim_start_time
                logger.info('Simulation ' +  sim_name + ' duration (esterna) -> ' + str(duration.total_seconds()) + 's')

            ##os.path.basename(fmu_path),
            
            # Prelevo timSim e LaneOffsetMedio dal file csv
            csv_file = os.path.join("/home/udineoffice/Desktop/SimulationLauncher/outputs", sim_output_folder, ".debug/Dati_rdbSniffer.csv")

            TimeSimulation = SelectFromCSV.TimeSimFromCSV(csv_file) #devo passargli il percorso cosi riesce a pescare il csv
            MediaLaneOffset = SelectFromCSV.MediaLaneOffsetFromCSV(csv_file)
            logger.info('\nTotal time of Simulation ' +  sim_name + ' -> ' + str(TimeSimulation) + 's')
            logger.info('MediaValue of LaneOffset of Simulation' +  sim_name + ' -> ' + str(MediaLaneOffset))

            logger.debug('Generating debug files...')
            with open(os.path.join(sim_output_debug_folder, 'driver_ctrl.csv'), 'w+') as dctl_out_csv, open('/tmp/taskRec_ModuleManager.txt', 'r') as mm_file:
                ##open(os.path.join(sim_output_debug_folder, 'fmu_io.csv'), 'w+') as fmu_out_csv,
                
                driver_time = 0.0
                ##fmu_time = 0.0,
                
                mm_fields_params = {
                    'DRIVER_CTRL,': {'file': dctl_out_csv, 'frame': driver_time}
                    ##'FMU IN/OUT,': {'file': fmu_out_csv, 'frame': fmu_time}
                }

                for line in mm_file.readlines():
                    mm_field = ''
                    for key, _ in mm_fields_params.items():
                        mm_field = key if key in line else mm_field
                    if mm_field != '':
                        new_line = line[line.index(mm_field) + len(mm_field):]
                        try:
                            new_time = float(new_line.split(',')[0])
                        except ValueError as e:
                            new_time = -1

                        if new_time != -1:
                            if new_time != mm_fields_params[mm_field]['frame'] and new_time != round(mm_fields_params[mm_field]['frame'] + 0.01, 2):
                                logger.warning('Skipped {field} time -> old frame: {old_frame} - new frame: {new_frame}'.format(field=mm_field[:-1],old_frame=mm_fields_params[mm_field]['frame'], new_frame=new_time))
                            mm_fields_params[mm_field]['frame'] = new_time
                        mm_fields_params[mm_field]['file'].write(new_line)
                        
            
            with open(os.path.join(sim_output_debug_folder, 'sim.info'), 'w+') as f:
                if not sim_completed:
                    f.write('+'*5+'SIM FAILED'+'+'*5 + '\n\n')
                f.write('Sim Name={sim_name}\n'.format(sim_name=sim_name))
                for key, value in sim_params.items():
                    f.write('{key}={value}\n'.format(key=key, value=value))
                f.write('Sim duration={duration}\n'.format(duration=duration))

            logger.info('Sim done\n\n')
            logger.info('Copying all the taskrec logs')
            for filename in glob.glob(os.path.join('/tmp', 'taskRec_*.txt')):
                logger.info('Copying: '+filename+' into '+ sim_output_debug_folder)
                shutil.copy(filename, sim_output_debug_folder)
                    
        #logger.info('Shrinking result files')
        #shrink_results(output_folder)
        #logger.info('Generating plots and pictures')
        #generate_post_processing_files(output_folder)
        
    logger.info('All done!')
