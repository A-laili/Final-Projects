from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import io
import base64

app = Flask(__name__)

# FCFS Scheduling
def fcfs_scheduling(tasks):
    tasks.sort(key=lambda x: x[1])  # Sort by arrival time
    current_time = 0
    gantt_chart = []
    waiting_times = {}

    for task in tasks:
        task_name, arrival_time, burst_time, deadline = task
        start_time = max(current_time, arrival_time)
        finish_time = start_time + burst_time
        gantt_chart.append((task_name, start_time, finish_time))
        waiting_time = start_time - arrival_time
        waiting_times[task_name] = waiting_time
        current_time = finish_time

    return gantt_chart, waiting_times, None  # FCFS doesn't return average waiting time

# Non-Preemptive SJF Scheduling
def non_preemptive_sjf(tasks):
    tasks.sort(key=lambda x: (x[1], x[2]))  # Sort by arrival time, then burst time
    current_time = 0
    gantt_chart = []
    waiting_times = {}
    task_completion_time = {}

    for task_name, arrival_time, burst_time, deadline in tasks:
        start_time = max(current_time, arrival_time)
        end_time = start_time + burst_time
        gantt_chart.append((task_name, start_time, end_time))
        task_completion_time[task_name] = end_time
        waiting_times[task_name] = start_time - arrival_time
        current_time = end_time

    average_waiting_time = sum(waiting_times.values()) / len(waiting_times)
    return gantt_chart, waiting_times, average_waiting_time

# Preemptive SJF Scheduling
def preemptive_sjf(tasks):
    tasks.sort(key=lambda x: (x[1], x[2]))  # Sort by arrival time, then burst time
    current_time = 0
    gantt_chart = []
    waiting_times = {}
    remaining_burst = {task[0]: task[2] for task in tasks}
    task_completion_time = {}

    while tasks or any(remaining_burst.values()):
        available_tasks = [task for task in tasks if task[1] <= current_time]

        if not available_tasks:
            current_time += 1
            continue

        next_task = min(available_tasks, key=lambda x: remaining_burst[x[0]])

        task_name, arrival_time, burst_time, deadline = next_task

        # Process the task for 1 time unit
        gantt_chart.append((task_name, current_time, current_time + 1))
        remaining_burst[task_name] -= 1
        current_time += 1

        # Remove completed tasks
        if remaining_burst[task_name] == 0:
            tasks = [task for task in tasks if task[0] != task_name]
            task_completion_time[task_name] = current_time
            waiting_times[task_name] = (
                current_time - arrival_time - burst_time
            )

    average_waiting_time = sum(waiting_times.values()) / len(waiting_times)
    return gantt_chart, waiting_times, average_waiting_time

# Earliest Deadline First Scheduling
def edf_scheduling(tasks):
    tasks.sort(key=lambda x: x[1])  # Sort by arrival time
    current_time = 0
    gantt_chart = []
    waiting_times = {}
    remaining_tasks = tasks[:]

    while remaining_tasks:
        ready_tasks = [task for task in remaining_tasks if task[1] <= current_time]

        if ready_tasks:
            task_name, arrival_time, burst_time, deadline = min(ready_tasks, key=lambda x: x[3])

            gantt_chart.append((task_name, current_time, current_time + 1))
            waiting_times[task_name] = current_time - arrival_time

            remaining_tasks = [
                task if task[0] != task_name else (task[0], task[1], task[2] - 1, task[3])
                for task in remaining_tasks
            ]
            remaining_tasks = [task for task in remaining_tasks if task[2] > 0]

            current_time += 1
        else:
            current_time += 1

    average_waiting_time = sum(waiting_times.values()) / len(waiting_times)
    return gantt_chart, waiting_times, average_waiting_time

# Least Laxity First Scheduling (LLF)
def llf_scheduling(tasks):
    tasks = [list(task) for task in tasks]  # Convert tuples to lists for mutation
    current_time = 0
    gantt_chart = []
    waiting_times = {}

    while tasks:
        # Compute laxity for each task
        task_laxity = {}
        for task in tasks:
            task_name, arrival_time, burst_time, deadline = task
            remaining_time = burst_time
            laxity = max(0, deadline - (current_time + remaining_time))  # Laxity = Deadline - (Current time + remaining time)
            task_laxity[task_name] = laxity

        # Check for the task with the minimum laxity
        if not task_laxity:
            break  # If no task has laxity, break the loop

        next_task_name = min(task_laxity, key=task_laxity.get)
        task = next((task for task in tasks if task[0] == next_task_name), None)

        if task:
            task_name, arrival_time, burst_time, deadline = task

            gantt_chart.append((task_name, current_time, current_time + 1))
            waiting_times[task_name] = current_time - arrival_time

            # Decrease burst time (remaining time)
            task[2] = max(0, task[2] - 1)  # Ensure burst_time doesn't go negative

            # If the task is finished, remove it from the tasks list
            if task[2] == 0:
                tasks.remove(task)

            current_time += 1

        # If no tasks are ready to execute, increment the time to avoid an infinite loop
        if not tasks:
            break

    average_waiting_time = sum(waiting_times.values()) / len(waiting_times)
    return gantt_chart, waiting_times, average_waiting_time

# Generate Gantt chart image
def generate_gantt_chart(gantt_chart, tasks):
    fig, ax = plt.subplots(figsize=(10, 4))
    colors = cm.get_cmap('Set1', len(tasks))
    task_colors = {task[0]: colors(i) for i, task in enumerate(tasks)}

    for task_name, start_time, end_time in gantt_chart:
        ax.barh("Tasks", end_time - start_time, left=start_time, color=task_colors.get(task_name, "gray"), edgecolor="black", label=task_name)
        ax.text((start_time + end_time) / 2, 0, task_name, ha="center", va="center", color="white", fontsize=10)

    ax.set_xlabel("Time", fontsize=12)
    ax.set_title("Gantt Chart", fontsize=14)
    ax.legend(fontsize=10)
    plt.xticks(fontsize=10)

    # Save to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        algorithm = request.form['algorithm']
        print(f"Selected Algorithm: {algorithm}")  # Debugging print statement
        num_tasks = int(request.form['num_tasks'])
        
        tasks = []
        for i in range(1, num_tasks + 1):
            try:
                name = request.form[f'name_{i}']
                arrival_time = int(request.form[f'arrival_{i}'])
                burst_time = int(request.form[f'burst_{i}'])
                deadline = int(request.form[f'deadline_{i}'])
                tasks.append((name, arrival_time, burst_time, deadline))
            except KeyError:
                return "Bad request, missing task fields", 400  # Handle missing fields

        if algorithm == "FCFS":
            gantt_chart, waiting_times, avg_waiting_time = fcfs_scheduling(tasks)
        elif algorithm == "SJF Preemptive":
            gantt_chart, waiting_times, avg_waiting_time = preemptive_sjf(tasks)
        elif algorithm == "SJF Non-Preemptive":
            gantt_chart, waiting_times, avg_waiting_time = non_preemptive_sjf(tasks)
        elif algorithm == "EDF":
            gantt_chart, waiting_times, avg_waiting_time = edf_scheduling(tasks)
        elif algorithm == "LLF":
            gantt_chart, waiting_times, avg_waiting_time = llf_scheduling(tasks)

        # Debugging the results of selected algorithm
        print(f"Gantt Chart: {gantt_chart}")
        print(f"Waiting Times: {waiting_times}")
        print(f"Average Waiting Time: {avg_waiting_time}")

        gantt_chart_img = generate_gantt_chart(gantt_chart, tasks)

        return render_template('index.html', gantt_chart_img=gantt_chart_img, waiting_times=waiting_times, avg_waiting_time=avg_waiting_time)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
