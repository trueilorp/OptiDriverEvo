import subprocess, logging, os, time, datetime, shutil, random, string, sys, glob
from os.path import dirname
from dotenv import load_dotenv  #libreria che semplifica l'uso di variabili d'ambiente, carica da pyenv le variabili
load_dotenv()
import selectFromCSV

from src.utils import DRIVER_PARAMS_LABEL_TO_NAME, read_configurations, configure_loggers, make_output_folders, copy_files
##from src.utils import FMU_DEFAULT_PATH, generate_fmu_mapping_car, fmu_mapping_car_path
from src.adams import shrink_results
from src.adams import TooManyResultsError, generate_post_processing_files

logging.getLogger('matplotlib').setLevel(logging.WARNING)

logger = logging.getLogger('root')
app_start = datetime.datetime.fromtimestamp(time.time()) #registra il modo in cui uno script viene avviato
launching_dir = os.getcwd() #setta la variabile launching_dir alla current working directory
configuration, sim_configuration = read_configurations(['config.json', 'sim_config.json'])
log_folder, output_folder = make_output_folders([configuration['logFolder'], configuration['outputFolder']], launching_dir, app_start)    
configure_loggers(log_folder, app_start)
logger.propagate = False #per evitare che si duplichino i logger
###START PROGRAM###

def scriptVTD (i):
    
    default_directory = '/home/udineoffice/Desktop/SimulationLauncher_PopulationBased'
    if os.getcwd() != default_directory:
        os.chdir(default_directory)
    
    try: #eccezione che mi manda un messaggio nel caso non venga trovata una configurazione del driver/scenario
        configuration, sim_configuration, driver_configuration = read_configurations(['config.json', 'sim_config.json', 'driver_config.json'])
    except FileNotFoundError as e:
        print('Missing configuration file.\n{error}'.format(error=str(e)))
        sys.exit(-1)  

    #print(driver_configuration)
    ## CREO LE CARTELLE DI OUTPUT CON LA FUNZIONE MAKE OUTPUT FOLDERS
    #crea una cartella per gli output ricevendo in input configuration che e la var. definita sopra

    #togliere i file che si creano dopo la simulazione all'interno della cartella tmp, sono i file delle finestre colorate che si aprono
    for filename in glob.glob(os.path.join('/tmp', 'taskRec_*.txt')):
        if os.path.exists(filename): 
            #logger.info('Clean: deleting '+ filename)
            os.remove(filename)            
        
    #copia i seguenti file nella cartella output_folders, per avere in ogni cartella di output anche la configurazione corrispondente
    #copy_files(['sim_config.json', 'driver_config.json'], output_folder)

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
            
            logger.info('Starting ' + sim_name) #inizio la simulazione
            logger.info('Killing previous instances...') #chiudo se ci sono altre simulazioni in corso, uso vtdStop.sh
            with subprocess.Popen(os.path.join(os.environ['VTD_ROOT'], 'bin', 'vtdStop.sh'), stdout=subprocess.PIPE, shell=True) as p: #reindirizzo lo standard output in una pipe cosi posso catturarlo
                logger.info('{p_out}'.format(p_out=p.stdout.read().decode('utf-8')))
            #time.sleep(seconds_between_processes)

            logger.info('Opening VTD') #apro VTD 
            vtd_launch_cmd =[os.path.join(os.environ['VTD_ROOT'], 'bin', 'vtdStart.sh'), '--project=' + os.environ['SM_SETUP'], '--autoConfig', '--setup=Standard.noGUInoIG'] 
            #logger.debug('Launch command -> ' + ' '.join(vtd_launch_cmd)) #lancio VTD con autoConfig/Standard.noIG  --setup=Standard.noGUInoIG --autoConfig
            #['/opt/MSC.Software/VTD.2023.2/bin/vtdStart.sh', '--project=SD_Project', '--autoConfig']
            vtd_process = subprocess.Popen(vtd_launch_cmd, stdout=vtd_out, stderr=vtd_out) #reindirizzamento standard output e standard error
            #logger.debug('VTD instance -> ' + str(vtd_process.pid)) #vtd_process l'ho definita sopra, con .pid prendo il PID del processo
            time.sleep(seconds_between_processes)

            #logger.debug('Launching SCP Monitor -> ' + ' '.join([os.path.join(os.environ['VTD_SCP_GENERATOR_EXE']), '-m'])) #genero SCP monitor
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
                #va ad impostare tutti i parametri del driver usando un file python che passa dall'etichetta al nome del parametro   
            command = command.no_wait().sim_ctrl(SCPCommand().self_closed_tag('Start')) #lancio la simulazione 
            
            launch_scp(command, scp_out, scp_out, 0)

            sim_output_folder = os.path.join(output_folder, scenario_file[:-4], driver_config_name, str(i) if 'driverConfigName' in sim_params.keys() else ''.join(random.choice(string.ascii_letters) for _ in range(6)))
            #logger.info('Creating output folder -> ' + str(sim_output_folder))
            sim_output_debug_folder = os.path.join(sim_output_folder, '.debug')
            os.makedirs(sim_output_debug_folder)

            shutil.copy("/home/udineoffice/Desktop/SimulationLauncher_PopulationBased/sim_config.json", sim_output_debug_folder)
            shutil.copy("/home/udineoffice/Desktop/SimulationLauncher_PopulationBased/driver_config.json", sim_output_debug_folder)

            rdbSniffer_output_file = os.path.join(sim_output_debug_folder, 'Dati_rdbSniffer.csv')
            #logger.info('Creating RDBSniffer output file -> ' + str(rdbSniffer_output_file))

            #logger.info('Opening rdbSniffer...') # + ' -c tcp -d -pkg 5 -csv prova'
            rdbSniffer_launch_cmd = [os.path.join(os.environ['RDB_ROOT'], 'rdbSniffer'),'-c', 'tcp', '-d', '-pkg', '5', '-csv', rdbSniffer_output_file] 
            #logger.debug('Launch command rdb -> ' + ' '.join(rdbSniffer_launch_cmd))
            rdbSniffer_process = subprocess.Popen(rdbSniffer_launch_cmd, stdout=rdb_out, stderr=rdb_out) #reindirizzamento standard output e standard error
            #logger.debug('RDB instance -> ' + str(rdbSniffer_process.pid)) #vtd_process l'ho definita sopra, con .pid prendo il PID del processo
            
            #Cercare di valutare ad ogni istante il laneOffset
            '''valutaLaneOffset_cmd = ["python3", "/home/udineoffice/Desktop/SimulationLauncher_PopulationBased/valutaLaneOffset.py"]
            logger.debug('Launch command valuta Lane Offset -> ' + ' '.join(valutaLaneOffset_cmd))
            valutaLaneOffset_process = subprocess.Popen(valutaLaneOffset_cmd, stdout=vlo_out, stderr=vlo_out) #reindirizzamento standard output e standard error
            logger.debug('Valuta Lane Offset instance -> ' + str(valutaLaneOffset_process.pid))
            time.sleep(seconds_between_processes)'''
            sim_completed = False
            
            try: #<Set entity="player" id="1" name="Ego"><PosInertial hDeg="-68.404" pDeg="3.386" rDeg="0.000" x="1508.011" y="-824.308" z="33.811" /></Set>
                #print('Waiting for out of road trigger...') 
                print('Waiting for stop trigger...')#<SimCtrl><DelayedStop value="true"/></SimCtrl>
                command = SCPCommand()\
                    .wait().sim_ctrl(SCPCommand().self_closed_tag('DelayedStop', {'value': 'true'}))\
                    .wait(1).cmd_enveloping_self_closed_tags('Symbol', {'name': 'exp101'},{
                        'Text': {'data': "Got trigger", 'colorRGB':"0xffff00", 'size':"50.0"},
                        'PosScreen': {'x':"0.01", 'y':"0.05"}
                    })
                launch_scp(command, out_handler=scp_out, error_handler=scp_out, timeout_min=int(configuration['simulationTimeoutMinutes']))
                #<Set entity="player" id="1" name="Ego"><PosInertial hDeg="-68.404" pDeg="3.386" rDeg="0.000" x="1508.011" y="-824.308" z="33.811" /></Set>
                logger.info('Scenario terminated')
                sim_completed = True #simulazione completata
            except subprocess.TimeoutExpired as e: #dopo 20 minuti killa la simulazione 
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
                '''logger.info('Killing ValutaLaneOffset...')
                try:
                    # Termina il processo utilizzando il suo PID
                    os.kill(valutaLaneOffset_process.pid, 9)  # Il segnale 9 è il segnale KILL, che forza la terminazione del processo
                    print(f"Processo con PID {valutaLaneOffset_process.pid} terminato con successo.")
                except ProcessLookupError:
                    print(f"Processo con PID {valutaLaneOffset_process.pid} non trovato.")
                except Exception as e:
                    print(f"Errore durante la terminazione del processo: {str(e)}")'''

                duration = datetime.datetime.now() - sim_start_time
                #logger.info('Simulation ' +  sim_name + ' duration (esterna) -> ' + str(duration.total_seconds()) + 's')

            ##os.path.basename(fmu_path)
            
            # Prelevo timeSim e LaneOffsetMedio dal file csv
            csv_file = os.path.join("/home/udineoffice/Desktop/SimulationLauncher_PopulationBased/outputs", sim_output_folder, ".debug/Dati_rdbSniffer.csv")

            time_simulation = selectFromCSV.get_time_sim_from_csv(csv_file) #devo passargli il percorso cosi riesce a pescare il csv
            max_lane_offset = selectFromCSV.get_max_lane_offset_from_csv(csv_file) 
            logger.info('\nTime of Simulation ' +  sim_name + ' -> ' + str(time_simulation) + 's')
            logger.info('Max value of LaneOffset of Simulation' +  sim_name + ' -> ' + str(max_lane_offset) + 'cm')

            #logger.debug('Generating debug files...')
            with open(os.path.join(sim_output_debug_folder, 'driver_ctrl.csv'), 'w+') as dctl_out_csv, open('/tmp/taskRec_ModuleManager.txt', 'r') as mm_file:
                
                driver_time = 0.0
                
                mm_fields_params = {
                    'DRIVER_CTRL,': {'file': dctl_out_csv, 'frame': driver_time}                    
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

            #logger.info('Sim ' + str(i) + ' done\n\n')
            #logger.info('Copying all the taskrec logs')
            for filename in glob.glob(os.path.join('/tmp', 'taskRec_*.txt')):
                shutil.copy(filename, sim_output_debug_folder)

    return (time_simulation, max_lane_offset)