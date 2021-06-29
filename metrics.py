import matplotlib.pyplot as plt


def check_if_congested(traffic_map, intersections):
    congested_intersections = 0
    for intersection in intersections:
        if traffic_map[intersection.position_x, intersection.position_y] == 1:
            congested_intersections += 1

    return congested_intersections


def plot_congested(congested_dir, timesteps):
    time = []
    for t in range(timesteps):
        time.append(t)
    for key, value in congested_dir.items():
        plt.plot(time, value, linewidth=1)
        plt.xlabel('Time (s)')
        plt.ylabel('Congested Intersections')

    plt.legend(["Cycle duration: 5 seconds", "Cycle duration: 10 seconds", "Cycle duration: 15 seconds", "Cycle duration: 20 seconds"], loc="lower right", fontsize=8)
    plt.savefig("congestion.png")

    avg = []
    for cycle, value in congested_dir.items():
        summary = 0
        for val in value:
            summary += val
        avg.append(summary)

    plt.figure()
    for val in avg:
        congestion_timestep = []
        val = val/timesteps
        for t in range(timesteps):
            congestion_timestep.append(val)
        plt.plot(time, congestion_timestep, linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Average Congested Intersections')
    plt.legend(["Cycle duration: 5 seconds", "Cycle duration: 10 seconds", "Cycle duration: 15 seconds", "Cycle duration: 20 seconds"], loc="lower right", fontsize=8)
    plt.savefig("average_congestion.png")


def plot_flow(flow_dict, timesteps):
    time = []
    plt.figure()
    for t in range(timesteps):
        time.append(t)
    for key, value in flow_dict.items():
        for val in range(len(value)):
            value[val] = value[val]*3600
        plt.plot(time, value, linewidth=1)

    plt.xlabel('Time (sec)')
    plt.ylabel(f'Flow Rate (vehicles/hour)')
    plt.legend(["Cycle duration: 5 seconds", "Cycle duration: 10 seconds", "Cycle duration: 15 seconds", "Cycle duration: 20 seconds"], loc="lower right", fontsize=8)
    plt.savefig("Flow_rate.png")

    avg = []
    for cycle, value in flow_dict.items():
        summary = 0
        for val in value:
            summary += val
        avg.append(summary)

    plt.figure()
    for val in avg:
        congestion_timestep = []
        val = val/timesteps
        for t in range(timesteps):
            congestion_timestep.append(val)
        plt.plot(time, congestion_timestep, linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Average Congested Intersections')
    plt.legend(["Cycle duration: 5 seconds", "Cycle duration: 10 seconds", "Cycle duration: 15 seconds", "Cycle duration: 20 seconds"], loc="lower right", fontsize=8)
    plt.savefig("average_flow.png")
