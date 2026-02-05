from a1Detector_project import percentages
from a1Detector_project_repetitions import word_repetitions
import matplotlib.pyplot as plt

data = percentages()
repetitions = word_repetitions()
magnitude_percentages = data["magnitude_percentages"]
reference_percentages = data["reference_percentages"]
rep = repetitions["repetitions"]
linebreak = "---------------------------------------"

def visuals(mag_percentages, ref_percentages):
    magnitudes = range(1, 9)
    plt.bar([x-0.2 for x in magnitudes], mag_percentages, width=0.4, label="Text in detection")
    plt.bar([x+0.2 for x in magnitudes], ref_percentages, width=0.4, label="Reference book")
    plt.xlabel("Zipf Magnitude")
    plt.ylabel("Percentage of words")
    plt.title("Word frequency distribution comparison")
    plt.legend()
    plt.show()
    
def main():
    print(linebreak)
    print(data["magnitude_percentages"])
    print(linebreak)
    print(rep)
    visuals(magnitude_percentages, reference_percentages)

if __name__ == "__main__":
    main()