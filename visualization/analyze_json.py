import os
import json
import statistics
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader

def load_demographics(agent_folder_path):
    demographics = []

    # Iterate through each agent folder
    for agent_folder in os.listdir(agent_folder_path):
        agent_path = os.path.join(agent_folder_path, agent_folder)
        if os.path.isdir(agent_path):
            scratch_file = os.path.join(agent_path, 'scratch.json')
            if os.path.isfile(scratch_file):
                with open(scratch_file, 'r') as f:
                    data = json.load(f)
                    demographics.append(data)

    return demographics

def calculate_statistics(demographics):
    attribute_stats = {}

    # Aggregate attributes
    for demo in demographics:
        for key, value in demo.items():
            if key not in attribute_stats:
                attribute_stats[key] = []
            attribute_stats[key].append(value)

    # Calculate statistics
    stats = {}
    for key, values in attribute_stats.items():
        try:
            stats[key] = {
                'mean': statistics.mean(values),
                'median': statistics.median(values),
                'stdev': statistics.stdev(values) if len(values) > 1 else 0,
                'min': min(values),
                'max': max(values)
            }
        except TypeError:
            # Handle non-numeric values
            stats[key] = {
                'mode': statistics.mode(values),
                'count': len(values),
                'categories': {val: values.count(val) for val in set(values)}
            }

    return stats

def plot_categorical_data(stats, plot_folder='plots'):
    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)

    for attribute, stat in stats.items():
        if 'categories' in stat:
            categories = stat['categories']
            plt.figure(figsize=(10, 5))
            plt.bar(categories.keys(), categories.values())
            plt.xlabel('Categories')
            plt.ylabel('Incidence')
            plt.title(f'Incidence of Categories for {attribute}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(plot_folder, f'{attribute}_categories.png'))
            plt.close()

def generate_html_report(stats, output_file='report.html', plot_folder='plots'):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('report_template.html')

    # Render the template with the statistics
    html_content = template.render(stats=stats, plot_folder=plot_folder)

    # Write the HTML content to a file
    with open(output_file, 'w') as f:
        f.write(html_content)

def main():
    agent_folder_path = '/Users/rgarzon/Documents/Stanford/genagents/agent_bank/populations/gss_agents'
    demographics = load_demographics(agent_folder_path)
    stats = calculate_statistics(demographics)

    # Display statistics
    for attribute, stat in stats.items():
        print(f"Statistics for {attribute}:")
        for stat_name, value in stat.items():
            if stat_name != 'categories':
                print(f"  {stat_name}: {value}")
        print()

    # Plot categorical data
    plot_categorical_data(stats)

    # Generate HTML report
    generate_html_report(stats)

if __name__ == "__main__":
    main()