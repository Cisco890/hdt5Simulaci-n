#####################################################################################################
#			Juan Francisco Martínez 23617
#			Hoja de trabajo 5
#####################################################################################################
import simpy
import random
import numpy as np

RANDOM_SEED = 42

class SistemaOperativo:
    def __init__(self, env, llegada, ram, velcpu):
        self.env = env
        self.llegada = llegada
        self.RAM = simpy.Container(env, init=ram, capacity=ram)
        self.CPU = simpy.Resource(env, capacity=1)
        self.velcpu = velcpu
        self.tiempos = []

    def llegada_proceso(self, proceso):
        yield self.env.timeout(random.expovariate(1.0 / self.llegada))
        self.env.process(self.ejecutar_proceso(proceso))

    def ejecutar_proceso(self, proceso):
        inicio_tiempo = self.env.now
        print(f"{inicio_tiempo}: Proceso {proceso} en estado 'new'")
        memoria = random.randint(1, 10)

        with self.RAM.get(memoria) as req:
            yield req

            print(f"{self.env.now}: Proceso {proceso} en estado 'ready'")
            instrucciones_restantes = random.randint(1, 10)

            while instrucciones_restantes > 0:
                with self.CPU.request() as req_cpu:
                    yield req_cpu
                    print(f"{self.env.now}: Proceso {proceso} en estado 'running'")
                    yield self.env.timeout(1 / self.velcpu)
                    instrucciones_restantes -= 3

                    if instrucciones_restantes <= 0:
                        estado_final = 'Terminated' if random.choice([True, False]) else 'Waiting' if random.randint(1, 21) == 1 else 'Ready'
                        print(f"{self.env.now}: Proceso {proceso} en estado '{estado_final}'")
                        if estado_final == 'Waiting':
                            yield self.env.timeout(1)
                            print(f"{self.env.now}: Proceso {proceso} en cola 'Ready'")
            self.RAM.put(memoria)
            fin_tiempo = self.env.now
            self.tiempos.append(fin_tiempo - inicio_tiempo)

def ejecutar_simulacion(num_procesos, llegada, ram, velcpu, num_cpus=1):
    env = simpy.Environment()
    env.process(simular_procesadores(env, num_cpus))
    
    sistema = SistemaOperativo(env, llegada, ram, velcpu)

    for i in range(num_procesos):
        env.process(sistema.llegada_proceso(i + 1))

    env.run()

    tiempos_promedio = np.mean(sistema.tiempos)
    desviacion_std = np.std(sistema.tiempos)

    return tiempos_promedio, desviacion_std

def simular_procesadores(env, num_cpus):
    yield env.timeout(0)  # Simulación de procesadores

# Solicitar al usuario la cantidad de procesos y la cantidad de intervalos
num_procesos_usuario = int(input("Ingrese la cantidad de procesos con los que desea trabajar: "))
num_intervalos_usuario = int(input("Ingrese la cantidad de intervalos con los que desea trabajar: "))

# Mostrar el tiempo promedio y la desviación estándar al final
print("Resultados finales:")
resultados = []

# Realizar simulación con intervalos proporcionados por el usuario
for intervalo in range(num_intervalos_usuario):
    tiempos_promedio, desviacion_std = ejecutar_simulacion(num_procesos_usuario, intervalo + 1, 100, 3)
    resultados.append((tiempos_promedio, desviacion_std))
    print(f"Intervalos {intervalo + 1}: Tiempo Promedio = {tiempos_promedio:.2f}, Desviación Estándar = {desviacion_std:.2f}")

