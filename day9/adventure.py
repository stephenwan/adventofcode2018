from collections import defaultdict


class Node():
    def __init__(self, marble, prev=None, post=None):
        self.value = marble
        self.prev = prev if prev is not None else self
        self.post = post if post is not None else self


class Game():
    def __init__(self, players):
        self.players = players
        self.step = 0
        self.lead_node = Node(0)
        self.scores = defaultdict(int)

    def current_player(self):
        return (self.step - 1) % self.players + 1

    def play(self):
        self.step += 1
        if self.step % 23 == 0:
            ref_node = self.lead_node
            for _ in range(7):
                ref_node = ref_node.prev
            score = ref_node.value
            self.lead_node = ref_node.post
            self.lead_node.prev = ref_node.prev
            self.lead_node.prev.post = self.lead_node
            self.scores[self.current_player()] += score + self.step
        else:
            ref_node = self.lead_node.post
            node = Node(self.step, ref_node, ref_node.post)
            node.prev.post = node
            node.post.prev = node
            self.lead_node = node
        # print(f'step {self.step} current {self.lead_node.value}')


def solve(n_players, n_marbles):
    game = Game(n_players)
    for _ in range(n_marbles):
        game.play()
    return max(game.scores.values())
