import numpy as np
import matplotlib.pyplot as plt

opérations = {}
ope_t = {}

class opération:
    def __init__(self,name, time, puissance, cycle = True):
        self.name = name
        self.time= time
        self.puissance = puissance
        self.cycle = cycle
        self.compteur = 0
            
class rover:
    def __init__(self):
        self.drymass = 207
        self.mass = self.drymass
        self.cruise_speed = 0.1

        self.solar_power = 91.5

        self.gravity = 1.62

        self.opérations_list = []

        self.n_cycle = 40

        self.time = 0

        self.battery_E = 350000
        self.initial_E = self.battery_E

        self.control_consumption = 65


    def power_rouler(self, vitesse = 0.1):
        Fs = 1
        mu_regolithe = 0.5
        mass = self.mass
        eff_moteur = 0.9
        eff_worm_gear = 0.9

        P = mu_regolithe*self.gravity*mass*vitesse/(eff_moteur*eff_worm_gear)

        return P*Fs


    def add_cycle_opération(self, oper):
        self.opérations_list.append(oper)



Rover = rover()

latence = opération(name = 'Latence (contrôle)', time = 3, puissance = 0,cycle = False)

rouler_aller = opération(name = 'Rouler (aller)', time= 450, puissance = 0, cycle = False)

moulin = opération(name = 'Moulin', time= 15, puissance = 24)
Rover.add_cycle_opération(moulin)

lever_moulin = opération('Lever Moulin',time= 10, puissance = 67)
Rover.add_cycle_opération(lever_moulin)

attendre_déversement = opération(name = 'Attente Déversement', time=40, puissance  = 0)
Rover.add_cycle_opération(attendre_déversement)

descendre_moulin = opération(name = 'Lever Moulin', time= 10, puissance = lever_moulin.puissance)
Rover.add_cycle_opération(descendre_moulin)


compactage = opération(name = 'Compactage', time=15, puissance = 30, cycle =  False)

débloquer_porte = opération(name = 'Loquet Porte Déchargement', time= 5, puissance = 8.8, cycle = False)
ouvrir_rampe = opération('Mouvement Porte Déchargement', time= 10, puissance = 28, cycle = False)
déchargement = opération('Déchargement', time= 20, puissance = 25, cycle = False)
fermeture_rampe = opération('Mouvement Porte Déchargement', time= 10, puissance = 28, cycle = False)
bloquer_porte = opération(name = 'Loquet Porte Déchargement', time= 5, puissance = 8.8, cycle = False)

rouler_retour = opération('Rouler (retour)', 450, puissance = 0, cycle = False)


def effectuer_opération(operation,vitesse = 0.01):

    

    operation_start_time = Rover.time
    if operation == déchargement:
        charge = Rover.mass - Rover.drymass


    while operation.time > (Rover.time - operation_start_time):

        if operation == rouler_retour or operation == rouler_aller:
            vitesse = Rover.cruise_speed

        if operation == déchargement:
            Rover.mass -= dt*(charge)/déchargement.time

        Rover.time += dt
        time.append(Rover.time)

        consumption = Rover.control_consumption + Rover.power_rouler(vitesse = vitesse) + operation.puissance - Rover.solar_power
        Consumption.append(consumption)


        efficacité_batterie = 0.1
        Rover.battery_E =  Rover.battery_E - (consumption*dt) - efficacité_batterie*abs(consumption*dt)
        Battery_state.append(Rover.battery_E)

        mass.append(Rover.mass)

        if operation not in opérations:
            opérations[operation.name] = consumption
            operation.compteur += 1
        else:
            opérations[operation.name] = (opérations[operation.name]*opération.compteur + consumption)/(operation.compteur+1)
            operation.compteur += 1

        if operation not in ope_t:
            ope_t[operation.name] = 1
            operation.compteur += 1
        else:
            ope_t[operation.name] += 1
            operation.compteur += 1

#t = 0
dt = 1
objectifs_de_cycles = Rover.n_cycle

mass = []
Battery_state = []
time  = []
Consumption = []

#first transport
effectuer_opération(latence, vitesse = 0)
effectuer_opération(rouler_aller)

import random
while Rover.n_cycle > 0:
    nombre_cycle_faits = objectifs_de_cycles - Rover.n_cycle
    #cycle du moulin
    for operation in Rover.opérations_list:
        effectuer_opération(latence,vitesse = 0)
        effectuer_opération(operation)

    Rover.mass = Rover.mass + 7.5 - 7.5*random.random()*0.3

    if (nombre_cycle_faits%8 == 0) and (nombre_cycle_faits != 0):
        effectuer_opération(compactage)
        effectuer_opération(latence,vitesse = 0)
        
    Rover.n_cycle -= 1
else:
    effectuer_opération(latence, vitesse = 0)
    effectuer_opération(rouler_retour)

    
    effectuer_opération(latence, vitesse=0)
    effectuer_opération(débloquer_porte, vitesse = 0)

    effectuer_opération(latence, vitesse = 0)
    effectuer_opération(ouvrir_rampe, vitesse = 0)

    '''Le compactage ici sert à pousser le regolithe'''
    effectuer_opération(latence, vitesse = 0)
    effectuer_opération(compactage)

    effectuer_opération(latence, vitesse = 0)
    effectuer_opération(déchargement, vitesse = 0.01)


    effectuer_opération(latence, vitesse = 0)
    effectuer_opération(fermeture_rampe,vitesse = 0)

    effectuer_opération(bloquer_porte, vitesse = 0)

    battery_start = False
    while Rover.battery_E <= Rover.initial_E:
        if not battery_start:
            start = Rover.time
            battery_start = True
        else:
            effectuer_opération(latence, vitesse =0)
    else:
        print(f'Temps de rechargement de la batterie de : {Rover.time - start} s')
        print(f'Capacité minimale de la batterie : {(max(Battery_state)-min(Battery_state))/1000:.2f} KJ')

import os

# Plot Power Consumption
scatter =False
if scatter:
    plt.scatter(time, Consumption, s=1)
else:
    plt.plot(time, Consumption, linewidth = 0.75)
plt.title('Puissance nette demandée')
plt.xlabel('Temps (s)')
plt.ylabel('Puissance demandée (w)')
plt.minorticks_on()
plt.grid(which='both', linestyle=':', linewidth='0.5', color='gray')
plt.show()
plt.savefig(os.getcwd() + '//Puissance')

# Plot Battery State
plt.plot(time, np.array(Battery_state) / 1000)
plt.title('Battery State Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Battery State (KJ)')
plt.minorticks_on()
plt.grid(which='both', linestyle=':', linewidth='0.5', color='gray')
plt.show()
plt.savefig('Batterie')

# Plot Rover Mass
plt.plot(time, mass)
plt.title('Rover Mass Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Rover Mass (Kg)')
plt.minorticks_on()
plt.grid(which='both', linestyle=':', linewidth='0.5', color='gray')
plt.show()
plt.savefig('Masse')


val = [val  for val in opérations.values()]

# Sort the keys and values based on the val values
sorted_items = sorted(zip(opérations.keys(), val), key=lambda x: x[1])
sorted_keys, sorted_values = zip(*sorted_items)



val = [val  for val in opérations.values()]

# Sort the keys and values based on the val values
sorted_items = sorted(zip(opérations.keys(), val), key=lambda x: x[1])
sorted_keys, sorted_values = zip(*sorted_items)

plt.barh(y=list(sorted_keys), width=sorted_values, height=0.75)

 # Increase title fontsize
plt.xlabel('Puissance nette nécessaire (w)', fontsize=14)  # Increase xlabel fontsize
plt.ylabel('Opérations', fontsize=14)  # Increase ylabel fontsize
plt.minorticks_on()
plt.tick_params(axis='both', which='major', labelsize=14)  
plt.grid(which='both', linestyle=':', linewidth='0.5', color='gray')
plt.show()