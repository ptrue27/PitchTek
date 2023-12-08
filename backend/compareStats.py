import numpy as np


class StatsComparator:
    def __init__(self):
        """
        Initialize the StatsComparator class.
        """
        pass

    def compare_stats(self, stats1, stats2):
        """
        Compare two sets of stats and estimate the chances of each winning.

        :param stats1: Array of stats for the first entity
        :param stats2: Array of stats for the second entity
        :return: A tuple containing the estimated chances of winning (stats1, stats2)
        """
        # Basic validation
        if len(stats1) != len(stats2):
            raise ValueError("Stats arrays must be of the same length.")

        # Simple comparison logic (can be replaced with more complex analysis)
        wins1, wins2 = 0, 0
        for s1, s2 in zip(stats1, stats2):
            if s1 > s2:
                wins1 += 1
            elif s2 > s1:
                wins2 += 1

        total_comparisons = len(stats1)
        chance1 = wins1 / total_comparisons
        chance2 = wins2 / total_comparisons

        return chance1, chance2


# Example usage
if __name__ == "__main__":
    comparator = StatsComparator()

    # Example stats (these should be replaced with actual stats)
    stats_team1 = np.array([80, 70, 75])
    stats_team2 = np.array([65, 85, 70])

    chances = comparator.compare_stats(stats_team1, stats_team2)
    print(
        f"Chances of winning: Team1: {chances[0]*100}%, Team2: {chances[1]*100}%")
