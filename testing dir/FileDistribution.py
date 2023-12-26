class FileDistribution:
    def __init__(self, num_nodes):
        self.clients = [f'client{i}' for i in range(1, num_nodes + 1)]

    def random_placement(self, fragments):
        placements = [{"client_name": random.choice(self.clients), "data": fragment, "fragment_number": i + 1} for
                      i, fragment in enumerate(fragments)]
        return placements

    def min_copysets_placement(self, fragments):
        counts = {client: 0 for client in self.clients}
        placements = []

        for i, fragment in enumerate(fragments):
            chosen_client = min(counts, key=counts.get)
            placements.append({"client_name": chosen_client, "data": fragment, "fragment_number": i + 1})
            counts[chosen_client] += 1

        return placements

    def buddy_approach_placement(self, fragments):
        pairs = [(self.clients[i], self.clients[i + 1]) for i in range(0, len(self.clients), 2)]
        placements = [{"client_name": random.choice(buddy_pair), "data": fragment, "fragment_number": i + 1} for
                      i, (buddy_pair, fragment) in enumerate(zip(pairs, fragments))]
        return placements