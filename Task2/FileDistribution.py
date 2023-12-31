import random

class FileDistribution:
    def __init__(self, num_nodes):
        self.clients = [f'client{i}' for i in range(1, num_nodes + 1)]

    def random_placement(self, fragments, replicas=1):
        placements = [
            {"client_name": random.choice(self.clients), "data": fragment, "fragment": i + 1, "replica": j + 1}
            for i, fragment in enumerate(fragments)
            for j in range(replicas)
        ]
        return placements

    def min_copysets_placement(self, fragments, replicas=1):
        counts = {client: 0 for client in self.clients}
        placements = []

        for i, fragment in enumerate(fragments):
            chosen_clients = sorted(counts, key=counts.get)[:replicas]
            for j, client in enumerate(chosen_clients):
                placements.append({"client_name": client, "data": fragment, "fragment": i + 1, "replica": j + 1})
                counts[client] += 1

        return placements

    def buddy_approach_placement(self, fragments, replicas=1):
        pairs = [(self.clients[i], self.clients[i + 1]) for i in range(0, len(self.clients), 2)]
        placements = [
            {"client_name": random.choice(buddy_pair), "data": fragment, "fragment": i + 1, "replica": j + 1}
            for i, (buddy_pair, fragment) in enumerate(zip(pairs, fragments))
            for j in range(replicas)
        ]
        return placements
