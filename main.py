import pygame

WIDTH = 800
TOTAL_BOXES_ROW = 50
TOTAL_BOXES_COLUMN = 50
WIDTH_BOX = 800 // TOTAL_BOXES_ROW
HEIGHT_BOX = 800 // TOTAL_BOXES_COLUMN
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
CAPTION = 'Breadth First Search Algorithm Visualization'
pygame.display.set_caption(CAPTION)

RED = (255, 0, 0)  # Goal Node Node
GREEN = (0, 255, 0)  # Start Node
PURPLE = (128, 0, 128)  # Path
WHITE = (255, 255, 255)  # Base Color
BLACK = (0, 0, 0)  # Barrier and Grid Lines
ORANGE = (255, 165, 0)  # Neighbours


def get_grid():
    complete_grid = []
    for row in range(TOTAL_BOXES_ROW):
        row_list = []
        for column in range(TOTAL_BOXES_COLUMN):
            row_list.append(Node(WHITE, WIDTH_BOX, HEIGHT_BOX, row, column))
        complete_grid.append(row_list)
    return complete_grid


def draw_lines(window):
    for i in range(TOTAL_BOXES_ROW):
        pygame.draw.line(window, BLACK,
                         (0, WIDTH_BOX * i),
                         (WIDTH, WIDTH_BOX * i), width=2)

    for j in range(TOTAL_BOXES_COLUMN):
        pygame.draw.line(window, BLACK,
                         (WIDTH_BOX * j, 0),
                         (WIDTH_BOX * j, WIDTH), width=2)


def draw_on_screen(grid):
    for i in grid:
        for j in i:
            j.draw(WINDOW)
    draw_lines(WINDOW)
    pygame.display.update()


class Node:
    def __init__(self, color, width, height, place_x, place_y):
        self.color = color
        self.width = width
        self.height = height
        self.no_x = place_x
        self.no_y = place_y
        self.neighbours = []
        self.visited = False
        self.parent = None

    def draw(self, window):
        pygame.draw.rect(window, self.color, ((self.no_x * self.width),
                                              (self.no_y * self.height),
                                              self.width,
                                              self.height))

    def reset(self):
        self.color = WHITE

    def make_start_node(self):
        self.color = GREEN

    def make_goal_node(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_neighbour(self):
        self.color = ORANGE

    def make_path(self):
        self.color = PURPLE

    def is_start_node(self):
        return self.color == GREEN

    def is_goal_node(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def update_neighbours(self, grid):
        if self.no_x < len(grid) - 1 and not grid[self.no_x + 1][self.no_y].is_barrier():  # DOWN CASE
            self.neighbours.append(grid[self.no_x + 1][self.no_y])
        if self.no_x > 0 and not grid[self.no_x - 1][self.no_y].is_barrier():  # UP CASE
            self.neighbours.append(grid[self.no_x - 1][self.no_y])
        if self.no_y < len(grid) - 1 and not grid[self.no_x][self.no_y + 1].is_barrier():  # RIGHT CASE
            self.neighbours.append(grid[self.no_x][self.no_y + 1])
        if self.no_y > 0 and not grid[self.no_x][self.no_y - 1].is_barrier():  # LEFT CASE
            self.neighbours.append(grid[self.no_x][self.no_y - 1])

    def is_equal(self, node):
        return self.no_x == node.no_x and self.no_y == node.no_x

    def __str__(self) -> str:
        return f'Color is: {self.color}\nWidth is: {self.width}\nHeight is: {self.height}\nNO_X: {self.no_x}\n' \
               f'NO_Y: {self.no_y}'

    def __repr__(self) -> str:
        return f'Color is: {self.color}, Width is: {self.width}, Height is: {self.height}, NO_X: {self.no_x}, ' \
               f'NO_Y: {self.no_y}'


def algorithm(start_node: Node, goal_node: Node, complete_grid):
    pass


def get_position(position_tuple):
    return position_tuple[0] // WIDTH_BOX, position_tuple[1] // HEIGHT_BOX


def reset_complete_grid():
    return get_grid()


def main():
    complete_grid = get_grid()
    start_node = None
    goal_node = None
    start_algo = True
    while start_algo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_algo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    complete_grid = reset_complete_grid()
                    start_node = None
                    goal_node = None
                if event.key == pygame.K_SPACE:

                    start_node.update_neighbours(complete_grid)
                    goal_node.update_neighbours(complete_grid)

                    queue = []
                    for i in start_node.neighbours:
                        i.parent = start_node
                        i.visited = True
                        queue.append(i)

                    is_algo_running = True
                    while len(queue) > 0 and is_algo_running:
                        node = queue.pop(0)
                        node.update_neighbours(complete_grid)
                        for j in node.neighbours:
                            if not j.is_start_node() and not j.is_goal_node():
                                j.make_neighbour()
                            if not j.visited:
                                j.visited = True
                                queue.append(j)
                                j.parent = node
                        if node.is_equal(goal_node):
                            is_algo_running = False
                        draw_on_screen(complete_grid)

                    n = goal_node
                    while n:
                        n.make_path()
                        draw_on_screen(complete_grid)
                        n = n.parent

            if pygame.mouse.get_pressed()[0]:
                x_val, y_val = get_position(pygame.mouse.get_pos())
                node_hovered = complete_grid[x_val][y_val]
                if not start_node and (not node_hovered.is_goal_node()):
                    node_hovered.make_start_node()
                    start_node = node_hovered
                elif start_node and not goal_node and not node_hovered.is_start_node():
                    node_hovered.make_goal_node()
                    goal_node = node_hovered
                elif not node_hovered.is_start_node() and not node_hovered.is_goal_node():
                    node_hovered.make_barrier()

            if pygame.mouse.get_pressed()[2]:
                x_val, y_val = get_position(pygame.mouse.get_pos())
                node_hovered = complete_grid[x_val][y_val]
                if node_hovered.is_start_node():
                    node_hovered.reset()
                    start_node = None
                elif node_hovered.is_goal_node():
                    node_hovered.reset()
                    goal_node = None
                elif node_hovered.is_barrier():
                    node_hovered.reset()
        draw_on_screen(complete_grid)


main()

