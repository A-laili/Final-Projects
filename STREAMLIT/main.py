import pandas as pd
import plotly
import streamlit as st
import plotly.figure_factory as ff
from fcfs import fcfs
from sjf import sjf_without_preemption
from sjf_p import sjf_with_preemption
from rm import rm
from dm import dm
from edf import edf

st.markdown("""
    <style>
        body {
            background-color: #87CEEB;  /* Bleu ciel */
            color: white;
            font-family: 'Arial', sans-serif;
        }
        
        /* Changer la couleur de fond des boutons */
        .stButton>button {
            background-color: #2a9d8f;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #264653;
        }

        /* Personnaliser la couleur de fond de la barre latérale */
        .css-1d391kg { 
            background-color: #1f1f1f; /* Couleur de fond de la sidebar */
        }

        /* Personnaliser la couleur du tableau de données */
        .stDataFrame {
            border: 1px solid #e1e1e1;
            padding: 10px;
            color: white;
        }

        /* Personnaliser les en-têtes du tableau */
        .stDataFrame th {
            background-color: #333333;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Function to display the results of an algorithm
def display_algorithm_results(algorithm_results):
    st.subheader(f"{algorithm_results['Algorithm']} Results:")
    st.bar_chart(algorithm_results["gantt_chart"])

def display_process_table(processes):
    """ Function to display the input process data as a table with a width setting """
    df_processes = pd.DataFrame(processes)
    st.dataframe(df_processes, width=700)  # Adjust the width as needed

def create_gantt_chart(c):
    """Function to create and display a Gantt chart"""
    gantt_data = []
    task_color = 'rgb(0, 0, 255)'
    
    # Iterate through the gantt_representation and create Gantt chart data
    current_time_slot = 0
    for task, duration in c:
        if task == 'Task No Task' or task == 'No Task':
            current_time_slot += duration
            continue  # Skip Task No Task
        gantt_data.append(
            dict(Task=task, Start=current_time_slot, Finish=current_time_slot + duration, Color=task_color))
        current_time_slot += duration

    # Create a Gantt chart figure
    fig = ff.create_gantt(
        gantt_data,
        show_colorbar=True,
        index_col='Task',
        group_tasks=True,
    )

    # Customize figure layout
    x_ticks = sorted(set(time for task in gantt_data for time in [task['Start'], task['Finish']]))
    x_ticks_str = [str(time % 60) for time in x_ticks]

    fig.update_layout(
        xaxis=dict(
            showgrid=True,
            tickvals=x_ticks,
            ticktext=x_ticks_str,
        ),
        yaxis=dict(
            showgrid=True,
        ),
        title_text='Gantt Chart',
        xaxis_title='Time Slots',
        yaxis_title='Tasks',
        xaxis_type='linear',
    )

    # Display the Gantt chart using Streamlit
    st.plotly_chart(fig)

def fcfs_page():
    st.subheader("Premier Arrivé, Premier Servi (FCFS)")

    # Obtenir le nombre de processus
    num_processes = st.number_input("Entrez le nombre de processus:", min_value=1, value=3, step=1)
    
    processes = []

    # Collecter les informations sur chaque processus
    for i in range(num_processes):
        process_data = {}
        process_data["Process"] = i + 1
        
        # Utilisation de deux colonnes pour l'entrée des données (temps d'arrivée et burst time)
        col1, col2 = st.columns(2)
        with col1:
            process_data["Arrival Time"] = st.number_input(f"Temps d'arrivée du processus {i + 1}:", min_value=0, value=0, step=1)
        with col2:
            process_data["Burst Time"] = st.number_input(f"Temps d'exécution du processus s {i + 1}:", min_value=1, value=5, step=1)
        
        processes.append(process_data)
    
   
    # Lorsque l'utilisateur clique sur "Run FCFS Algorithm"
    if st.button("Exécuter l'algorithme FCFS"):
        waiting_times, average_waiting_time, gantt_chart = fcfs(processes)
        st.text(f"Temps d'attente: {waiting_times}")
        st.text(f"Temps d'attente moyen: {average_waiting_time}")
        st.text(f"Gantt chart: {gantt_chart}")
        create_gantt_chart(gantt_chart)

def sjf_page():
    st.subheader("Shortest Job First (SJF) sans Preemption")
    
    num_processes = st.number_input("Entrez le nombre de processus:", min_value=1, value=3, step=1)
    processes = []
    for i in range(num_processes):
        col1, col2 = st.columns(2)
        with col1:
            arrival_time = st.number_input(f"Temps d'arrivée du processus{i + 1}:", min_value=0, value=0, step=1)
        with col2:
            burst_time = st.number_input(f"Temps d'exécution du processus   {i + 1}:", min_value=1, value=5, step=1)
        processes.append({"Process": i + 1, "Arrival Time": arrival_time, "Burst Time": burst_time})

   
    if st.button("Run SJF Without Preemption Algorithm"):
        a, b, c = sjf_without_preemption(processes)
        st.text(f"waiting_times: {a}")
        st.text(f"average_waiting_time: {b}")
        st.text(f"gantt_chart: {c}")
        create_gantt_chart(c)

def sjf_preemption_page():
    st.subheader("Shortest Job First (SJF) avec Preemption")

    num_processes = st.number_input("Entrez le nombre de processus:", min_value=1, value=3, step=1)
    processes = []
    for i in range(num_processes):
        col1, col2 = st.columns(2)
        with col1:
            arrival_time = st.number_input(f"Temps d'arrivée du processus{i + 1}:", min_value=0, value=0, step=1)
        with col2:
            burst_time = st.number_input(f"Temps d'exécution du processus   {i + 1}:", min_value=1, value=5, step=1)
        processes.append({"Process": i + 1, "Arrival Time": arrival_time, "Burst Time": burst_time})

   

    if st.button("Run SJF With Preemption Algorithm"):
        a, b, c = sjf_with_preemption(processes)
        st.text(f"waiting_times: {a}")
        st.text(f"average_waiting_time: {b}")
        st.text(f"gantt_chart: {c}")
        create_gantt_chart(c)

def DM_page():
    st.subheader("Deadline Monothonic - DM")

    num_processes = st.number_input("Entrez le nombre de processus:", min_value=1, value=3, step=1)
    processes = []
    for i in range(num_processes):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            arrival_time = st.number_input(f"Temps d'arrivée du processus{i + 1}:", min_value=0, value=0, step=1)
        with col2:
            burst_time = st.number_input(f"Temps d'exécution du processus   {i + 1}:", min_value=1, value=1, step=1)
        with col3:
            deadline = st.number_input(f"delai du processus  {i + 1}:", min_value=0, value=0, step=1)
        with col4:
            period = st.number_input(f"Periode du processus  {i + 1}:", min_value=1, value=1, step=1)
        processes.append({"Process": i + 1, "Task": i + 1, "Arrival Time": arrival_time, "Burst Time": burst_time, "Deadline": deadline, "Period": period})

   

    if st.button("Run DM Algorithm"):
        c = dm(processes)
        st.text(f"gantt_chart: {c}")
        create_gantt_chart(c)

def RM_page():
    st.subheader("Rate Monothonic - RM")

    num_processes = st.number_input("Entrez le nombre de processus:", min_value=1, value=3, step=1)
    processes = []
    for i in range(num_processes):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            arrival_time = st.number_input(f"Temps d'arrivée du processus{i + 1}:", min_value=0, value=0, step=1)
        with col2:
            burst_time = st.number_input(f"Temps d'exécution du processus   {i + 1}:", min_value=1, value=1, step=1)
        with col3:
            deadline = st.number_input(f"delai du processus  {i + 1}:", min_value=0, value=0, step=1)
        with col4:
            period = st.number_input(f"Periode du processus  {i + 1}:", min_value=1, value=1, step=1)
        processes.append({"Process": i + 1, "Task": i + 1, "Arrival Time": arrival_time, "Burst Time": burst_time, "Deadline": deadline, "Period": period})

    

    if st.button("Run RM Algorithm"):
        c = rm(processes)
        st.text(f"gantt_chart: {c}")
        create_gantt_chart(c)

def EDF_page():
    st.subheader("Earliest Deadline First - EDF")

    num_processes = st.number_input("Entrez le nombre de processus:", min_value=1, value=3, step=1)
    processes = []
    for i in range(num_processes):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            arrival_time = st.number_input(f"Temps d'arrivée du processus{i + 1}:", min_value=0, value=0, step=1)
        with col2:
            burst_time = st.number_input(f"Temps d'exécution du processus   {i + 1}:", min_value=1, value=1, step=1)
        with col3:
            deadline = st.number_input(f"delai du processus  {i + 1}:", min_value=0, value=0, step=1)
        with col4:
            period = st.number_input(f"Periode du processus  {i + 1}:", min_value=1, value=1, step=1)
        processes.append({"Process": i + 1, "Task": i + 1, "Arrival Time": arrival_time, "Burst Time": burst_time, "Deadline": deadline, "Period": period})

   
    if st.button("Run EDF Algorithm"):
        c = edf(processes)
        st.text(f"gantt_chart: {c}")
        create_gantt_chart(c)

# Main function to choose the algorithm
def main():
    st.title("Algorithmes d'ordonnancement")
    
    algorithm_choice = st.selectbox("Choisissez un algorithme d'ordonnancement", [
        "FCFS", "SJF without Preemption", "SJF with Preemption", "Deadline Monotonic", "Rate Monotonic", "Earliest Deadline First"
    ])

    if algorithm_choice == "FCFS":
        fcfs_page()
    elif algorithm_choice == "SJF without Preemption":
        sjf_page()
    elif algorithm_choice == "SJF with Preemption":
        sjf_preemption_page()
    elif algorithm_choice == "Deadline Monotonic":
        DM_page()
    elif algorithm_choice == "Rate Monotonic":
        RM_page()
    elif algorithm_choice == "Earliest Deadline First":
        EDF_page()

if __name__ == "__main__":
    main()
