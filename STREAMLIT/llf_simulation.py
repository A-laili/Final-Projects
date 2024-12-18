import streamlit as st
import pandas as pd
import plotly.figure_factory as ff

# Fonction de l'algorithme LLF
def llf_scheduler(tasks, simulation_time):
    schedule = []
    remaining_time = {task['name']: task['execution_time'] for task in tasks}
    deadlines = {task['name']: task['arrival_time'] + task['deadline'] for task in tasks}
    time = 0

    while time < simulation_time:
        # Calculer la laxité pour chaque tâche
        laxity = {}
        for task in tasks:
            name = task['name']
            if remaining_time[name] > 0:
                laxity[name] = deadlines[name] - time - remaining_time[name]
            else:
                laxity[name] = float('inf')  # Ignorer les tâches terminées

        # Sélectionner la tâche avec la laxité la plus faible
        current_task = min(laxity, key=laxity.get)
        if laxity[current_task] == float('inf'):  # Aucune tâche restante
            schedule.append((time, "No Task", 1))
        else:
            schedule.append((time, current_task, 1))
            remaining_time[current_task] -= 1

            # Mise à jour du délai si une tâche se répète périodiquement
            if remaining_time[current_task] == 0:
                remaining_time[current_task] = [t['execution_time'] for t in tasks if t['name'] == current_task][0]
                deadlines[current_task] += [t['period'] for t in tasks if t['name'] == current_task][0]

        time += 1

    return schedule

# Fonction pour créer le Gantt chart avec Plotly
def create_gantt_chart(schedule):
    gantt_data = []
    for time, task, duration in schedule:
        if task == "No Task":
            continue
        gantt_data.append(
            dict(Task=task, Start=time, Finish=time + duration, Resource=task)
        )

    fig = ff.create_gantt(
        gantt_data,
        show_colorbar=True,
        index_col='Resource',
        group_tasks=True,
        showgrid_x=True,
        showgrid_y=True
    )
    fig.update_layout(title="Diagramme de Gantt - LLF", xaxis_title="Temps", yaxis_title="Tâches")
    st.plotly_chart(fig)

# Interface utilisateur Streamlit
def main():
    st.title("Simulation de l'algorithme LLF (Least Laxity First)")

    # Sidebar pour les paramètres des tâches
    st.sidebar.header("Configuration des tâches")
    num_tasks = st.sidebar.number_input("Nombre de tâches", min_value=1, max_value=10, value=3, step=1)

    tasks = []
    for i in range(num_tasks):
        st.sidebar.subheader(f"Tâche {i+1}")
        name = st.sidebar.text_input(f"Nom de la tâche {i+1}", f"T{i+1}")
        execution_time = st.sidebar.number_input(f"Temps d'exécution (C{i+1})", min_value=1, value=1, step=1)
        arrival_time = st.sidebar.number_input(f"Temps d'arrivée (A{i+1})", min_value=0, value=0, step=1)
        deadline = st.sidebar.number_input(f"Deadline (D{i+1})", min_value=1, value=5, step=1)
        period = st.sidebar.number_input(f"Période (P{i+1})", min_value=1, value=10, step=1)
        tasks.append({
            "name": name,
            "execution_time": execution_time,
            "arrival_time": arrival_time,
            "deadline": deadline,
            "period": period
        })

    simulation_time = st.sidebar.number_input("Durée de la simulation", min_value=10, value=20, step=1)

    if st.sidebar.button("Exécuter l'algorithme LLF"):
        st.subheader("Tâches saisies")
        st.dataframe(pd.DataFrame(tasks))

        st.subheader("Résultats de la simulation")
        schedule = llf_scheduler(tasks, simulation_time)
        create_gantt_chart(schedule)

if __name__ == "__main__":
    main()
