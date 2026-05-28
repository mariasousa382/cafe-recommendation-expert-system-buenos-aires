# Buenos Aires Cafe Expert System

An AI-powered expert system built with Python and Prolog that recommends cafés in Buenos Aires based on student preferences such as distance, budget, Wi-Fi quality, outlets, noise level, crowdedness, food options, and café size.

This project was created for CS152 - Harnessing Artificial Intelligence Algorithms at Minerva University.

### Overview

Finding cafés that are suitable for studying in a new city can be difficult, especially for students with specific needs like reliable Wi-Fi, power outlets, quiet environments, or late closing times.

This expert system helps users discover cafés near the Minerva residence hall in Buenos Aires by asking a sequence of preference-based questions and filtering cafés using rule-based logical inference.

The system combines:

- Python for the command-line interface and user interaction
- Prolog for the knowledge base and reasoning engine
- pyswip as the bridge between Python and Prolog

### Features
- Rule-based expert system
- Interactive command-line interface
- Multi-criteria café filtering
- Dynamic preference matching
- Real café dataset collected in Buenos Aires
- Prolog logical inference
- Early stopping when no cafés match user criteria

### Technologies Used
- Python
- Prolog
- pyswip

### How It Works

The system stores cafés as Prolog facts, where each café contains attributes such as:

- Distance
- Budget
- Outlets availability
- Noise level
- Crowdedness
- Goods offered
- Closing time
- Wi-Fi quality
- Size

The user answers a sequence of menu-based questions. Their preferences are dynamically asserted into the Prolog knowledge base, and the system filters cafés using logical inference through the matches_criteria/1 predicate.

If cafés match all selected criteria, the system returns the matching recommendations.

### Example Interaction
Welcome to the Buenos Aires Cafe Finder!

How far are you willing to walk to the cafe?
1. Less than 1 km
2. 1-2 km
3. 2-3 km
4. Over 3 km

What's your budget per person?
1. Under 10k
2. 10k-20k
3. Over 20k

...

Found 2 matching cafe(s):
1. Divino Budin
2. Posdata Cafe Postal

### Installation

Clone the repository:

git clone https://github.com/mariasousa382/cafe-recommendation-expert-system-buenos-aires.git
cd buenos-aires-cafe-expert-system

Install dependencies:

pip install -r requirements.txt

### Running the Project
python cafes.py

### Data Collection

The café data was collected from:

- Google Maps
- Café websites
- Personal visits and observations

The dataset includes 23 cafés near the Minerva residence hall in Buenos Aires.

### Future Improvements
- Web interface
- Interactive map integration
- Real-time café data
- Personalized recommendation history
- Machine learning ranking system

### Authors

Created as a group project for CS152 at Minerva University.

Contributors: Emma, Anhelina, Dasha, Maria
