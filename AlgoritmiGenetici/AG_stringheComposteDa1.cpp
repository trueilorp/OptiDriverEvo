#include <iostream>
#include <vector>
#include <random>

const int POPULATION_SIZE = 10;
const int CHROMOSOME_LENGTH = 5;
const double MUTATION_RATE = 0.01;

using namespace std;

// Funzione per calcolare la fitness di un cromosoma
int fitness(const vector<int>& chromosome) {
    int score = 0;
    for (int gene : chromosome) {
        score += gene; //sommo gli 0 e 1 all'interno del programma, se e formata da tutti 1 la somma sara uguale alla lunghezza 
    }
    return score;
}

// Funzione per selezionare un cromosoma basato sulla roulette wheel selection
int select(const vector<vector<int>>& population) { //riceve come parametro la matrice passata attraverso due puntatori 
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0, 1);
    double threshold = dis(gen);
    
    double cumulativeFitness = 0.0;
    for (int i = 0; i < POPULATION_SIZE; ++i) {
        cumulativeFitness += static_cast<double>(fitness(population[i])) / fitness(population[0]);
        if (cumulativeFitness >= threshold) {
            return i;
        }
    }
    
    return 0; // Fallback
}

// Funzione per eseguire la mutazione su un cromosoma, quindi cambio solo 1 gene in teoria, quello che ha una determinata probabilita
void mutate(vector<int>& chromosome) {
    random_device rd;
    mt19937 gen(rd()); //Mersenne Twister --> algoritmo generatore di numeri casuali
    uniform_real_distribution<> dis(0, 1); //genera un numero casuale distribuito tra 0 e 1 
    
    for (int& gene : chromosome) { //siccome c'e' & le modifiche verranno applicate anche all'oggetto chromosome
        if (dis(gen) < MUTATION_RATE) {
            gene = 1 - gene; // Flip the bit, ovvero lo faccio diventare l'opposto
        }
    }
}

int main() {
    // Inizializzazione della popolazione in modo casuale, population e' una matrice
    vector<vector<int>> population(POPULATION_SIZE, vector<int>(CHROMOSOME_LENGTH)); //dentro le parentesi ho le due dimensioni della matrice
    for (int i = 0; i < POPULATION_SIZE; ++i) {
        for (int j = 0; j < CHROMOSOME_LENGTH; ++j) {
            population[i][j] = rand() % 2; //qualsiasi numero modulo 2 ritorna o 0 o 1
        }
    }

    int generation = 0;
    while (1) //come dire while (true)
    {
        // Seleziona due genitori
        int parent1 = select(population);
        int parent2 = select(population);

        // Crea un figlio incrociando i genitori
        vector<int> child(CHROMOSOME_LENGTH);
        int crossoverPoint = rand() % CHROMOSOME_LENGTH; //scelgo un punto a casa di crossover
        for (int i = 0; i < crossoverPoint; ++i) {
            child[i] = population[parent1][i];
        } //il figlio avra dall'inizio al crossover i geni del padre, dal crossover in poi quelli della madre 
        for (int i = crossoverPoint; i < CHROMOSOME_LENGTH; ++i) {
            child[i] = population[parent2][i];
        }

        // Applica mutazione al figlio
        mutate(child); //muto il vettore del figlio

        // Creo la nuova popolazione inserendo il figlio
        // Sostituisci il cromosoma meno adatto nella popolazione con il figlio
        int worstIndex = 0;
        int worstFitness = fitness(population[0]); //partiamo dal primo cromosoma e vediamo quanti 1 ha 
        for (int i = 1; i < POPULATION_SIZE; ++i) {
            int currentFitness = fitness(population[i]);
            if (currentFitness < worstFitness) {  //guardo nel mio vettore population se il cromosoma corrente e' peggio di quello di riferimento
                worstFitness = currentFitness;
                worstIndex = i;
            }
        }
        population[worstIndex] = child; //sostituisco il cromosoma peggiore con il figlio che avevo creato prima 

        // Controlla se abbiamo trovato una soluzione, all'interno sono all'interno di un while true quindi vado avanti 
        if (worstFitness == CHROMOSOME_LENGTH) {
            cout << "Generazione " << generation << ": Soluzione trovata!" << endl;
            break; //esco dal while
        }

        ++generation; //tengo conto di tutte i nuovi figli che ogni volta creo
    }

    return 0;
}
