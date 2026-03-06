import random
import csv
import math
import statistics

class Bin:
    def __init__(self, dices):
        self.start = dices
        self.end = dices * 6

    def create_bin(self):
            return list(range(self.start, self.end + 1))

    def bin_count(self, rolls):
        self.create_bin()
        count = {i: 0 for i in range(self.start, self.end + 1)}
        for roll in rolls:
            count[roll] += 1
        return count

class Dice:
    def __init__(self, dices, sides = 6):
        self.sides = sides
        self.dices = dices


    def roll(self):
        total = 0
        for _ in range(self.dices):
            total += random.randint(1, self.sides)
        return total
    
    def roll_multiple(self, times):
        return [self.roll() for _ in range(times)]

class Simulation:

    def __init__(self):
        self.dices = 0
        self.rolls = 0
        self.std_dev = 0
        self.mean = 0
        self.normal_dist = 0
        self.pdf = []
        

    def run_simulation(self, dices, times):
        dice = Dice(dices)
        self.dices = dices
        rolls = dice.roll_multiple(times)
        self.rolls = times
        bin = Bin(dices)
        self.std_dev = statistics.stdev(rolls)
        self.mean = statistics.mean(rolls)
        self.normal_dist = statistics.NormalDist(mu=self.mean, sigma=self.std_dev)
        for i in range(self.dices, self.dices * 6 + 1):
            self.pdf.append(self.normal_dist.pdf(i))
        self.print_results(bin.bin_count(rolls))
    
    def print_results(self, results):
        for total, count in results.items():
            print(f"Total: {total}, Count: {count}")
        self.write_data(results)
    
    def write_data(self, data, file_path = "DavidResults.md"):
        with open(file_path, mode='w') as file: 
            writer = csv.writer(file)
            #writer = csv.QUOTE_NONE(file)
            #header = str(f'***\nSimulation of {self.dices} dice for {self.rolls} rolls\n***\n\n')
            #print(header)
            writer.writerow(['***'])
            writer.writerow([f'Simulation of {self.dices} dice for {self.rolls} rolls'])
            writer.writerow(['***'])
            writer.writerow([])
            writer.writerow([])
            writer.writerow(['Dice Total', '\t\tCount', '\tPDF', '\tcurve'])
            for roll in data:
                if len(str(data[roll])) > 2:
                    writer.writerow([f"{roll}:" + f"\t\t\t\t{data[roll]}:" + f"\t{self.pdf[roll - self.dices]:.2f}:" "\t" + f"{'*' * math.ceil(self.pdf[roll - self.dices] * 100)}"])
                else:
                    writer.writerow([f"{roll}:" + f"\t\t\t\t{data[roll]}:" + f"\t\t{self.pdf[roll - self.dices]:.2f}:"+ "\t" + f"{'*' * math.ceil(self.pdf[roll - self.dices] * 100)}"])
                

def main():
    Simulation().run_simulation(2, 1000)

if __name__ == "__main__":
    main()