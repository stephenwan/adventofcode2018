class Recipe():
    def __init__(self, score, prev=None, post=None):
        self.score = score
        self.prev = prev if prev is not None else self
        self.post = post if post is not None else self


class Chain():
    def __init__(self):
        self.start = None
        self.end = None
        self.length = 0

    def add(self, score, on_add=None):
        recipe = Recipe(score)
        if self.start is None:
            self.start, self.end = (recipe, recipe)
        else:
            self.start.prev, self.end.post = (recipe, recipe)
            recipe.prev, recipe.post = (self.end, self.start)
            self.end = recipe
        self.length += 1
        if on_add is not None:
            on_add(recipe, self.length)
        return recipe

    def recipe_at(self, i, start=None):
        cur = self.start if start is None else start
        for _ in range(i):
            cur = cur.post
        return cur

    def recipe(self):
        yield self.start
        cur = self.start.post
        while cur != self.start:
            yield cur
            cur = cur.post

    def scores(self):
        for r in self.recipe():
            yield r.score

    def generate_recipes(self, r1, r2, on_add=None):
        high, low = divmod(r1.score + r2.score, 10)
        if high > 0:
            self.add(high, on_add)
        self.add(low, on_add)


def visualize(elf_angular, elf_square, chain):
    symbols = []
    for recipe in chain.recipe(False):
        if elf_angular == recipe:
            symbols.append(f'({recipe.score})')
        elif elf_square == recipe:
            symbols.append(f'[{recipe.score}]')
        else:
            symbols.append(f'{recipe.score}')
    print(' '.join(symbols))


class Done(Exception):
    pass


def solver(on_add):
    chain = Chain()
    elf_angular = chain.add(3)
    elf_square = chain.add(7)
    while True:
        # visualize(elf_angular, elf_square, chain)
        try:
            chain.generate_recipe(elf_angular, elf_square, on_add)
        except Done:
            break
        elf_angular = chain.recipe_at(elf_angular.score + 1, elf_angular)
        elf_square = chain.recipe_at(elf_square.score + 1, elf_square)


def solve_part1(pratice_recipe):
    ten_scores = []

    def on_add(recipe, length):
        if length > pratice_recipe:
            if len(ten_scores) == 10:
                raise Done()
            else:
                ten_scores.append(str(recipe.score))

    solver(on_add)
    return ''.join(ten_scores)


def solve_part2(target):
    target_list = list(str(target))

    holder = [''] * len(target_list)
    result_length = 0

    def on_add(recipe, length):
        nonlocal result_length
        holder.pop(0)
        holder.append(str(recipe.score))
        if holder == target_list:
            result_length = length - len(target_list)
            raise Done()

    solver(on_add)
    return result_length
