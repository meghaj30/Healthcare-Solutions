import sys
from random_forest_ml import RandomForestMLEngine

# Redirect print to a log file
log_file = open('test_ml_log.txt', 'w')
sys.stdout = log_file
sys.stderr = log_file

try:
    print("Testing Random Forest ML Engine...")
    engine = RandomForestMLEngine()
    insights = engine.generate_comprehensive_insights()
    print("\nGenerated Insights Successfully!")
    print("\n--- Data Summary ---")
    print(f"Total Patients: {insights['summary']['total_patients_analyzed']}")
    print("\n--- Visit Predictions ---")
    for day in insights['visit_analysis']['visit_predictions']['weekly_forecast']:
        print(f"{day['day_name']}: {day['predicted_visits']} visits")
    print("\n--- Top Diseases ---")
    for disease in insights['disease_analysis']['disease_distribution'][:3]:
        print(f"{disease['disease']}: {disease['cases']} cases ({disease['prevalence_rate']}%)")
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
finally:
    log_file.close()
    print("Done! Check test_ml_log.txt for details.")
