#####################################
#  SNAKE AI MADE BY SILVIAN ACHIM
# YOUTUBE: https://www.youtube.com/channel/UCWQRzGZa2Owh4U81pEQkObg

import snake
import pygame
import os
import neat
import pickle

pygame.font.init()

LENGTH = 10  # 35 for 35x35
WIDTH = 10  # 35 for 35x35
size = 98  # 28 for 35x35
w = size * LENGTH
h = size * WIDTH
STAT_FONT = pygame.font.SysFont("comicsans", 38)

draw = True

ind = 0
max_fitness = 0
gen = 0
max_score = 0

win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Snake ML made by Silvian Achim")
bush = pygame.image.load(os.path.join("images", "fruit.png"))
bg = pygame.image.load(os.path.join("images", "bg.png"))
face = pygame.image.load(os.path.join("images", "face.png"))
body = pygame.image.load(os.path.join("images", "body.png"))


def replay_genome(config_path, genome_path="winner.pkl"):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)
    print(genome)
    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    main(genomes, config)
    # return genomes


def main(genomes, config):
    global win, gen, draw, max_fitness, ind, max_score
    gen += 1

    nets = []
    snakes = []
    ge = []

    max_fitness = 0
    o = 0
    for genome_id, genome in genomes:
        try:
            if genome.fitness > max_fitness:
                max_fitness = genome.fitness
                ind = o
        except:
            pass
        o += 1
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(snake.Snake())
        ge.append(genome)
    for i, x in enumerate(snakes):
        x.reset()
        draw = True
    clock = pygame.time.Clock()
    active = True
    loop = 0
    while active and len(snakes) > 0:
        loop += 1
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.quit()
                quit()
                break
        for x, snk in enumerate(snakes):
            snakes[x].game()
            output = nets[x].activate((snakes[x].vision2()))
            for i in range(0, 3):
                if max(output) == output[i]:
                    if i == 0:  # Right
                        if snakes[x].direction == 0:
                            snakes[x].direction = 1
                        elif snakes[x].direction == 1:
                            snakes[x].direction = 3
                        elif snakes[x].direction == 3:
                            snakes[x].direction = 2
                        elif snakes[x].direction == 2:
                            snakes[x].direction = 0
                        break
                    elif i == 1:  # Forward
                        break
                    elif i == 2:  # Left
                        if snakes[x].direction == 0:
                            snakes[x].direction = 2
                        elif snakes[x].direction == 2:
                            snakes[x].direction = 3
                        elif snakes[x].direction == 3:
                            snakes[x].direction = 1
                        elif snakes[x].direction == 1:
                            snakes[x].direction = 0
                        break
        for x, snk in enumerate(snakes):
            if loop == 1:
                snk.loop_tail = snk.tail
            if loop == 250:
                loop = 0
                if snk.tail == snk.loop_tail:
                    ge[x].fitness -= (9000000 - snk.tail)
                    snk.gameOver = 3
            if snk.gameOver > 0:
                if x == ind:
                    draw = False
                if snk.score > max_score:
                    if x == ind:
                        max_score = snk.score
                ge[x].fitness -= 1000
                nets.pop(x)
                ge.pop(x)
                snakes.pop(x)
                if x < ind and draw:
                    ind -= 1

            if snk.eat and snk.gameOver == 0:
                ge[x].fitness += 100  # Food
                snakes[x].eat = False

        win.blit(bg, (0, 0))
        try:
            if snakes[ind].gameOver == 0 and draw:  # And draw
                win.blit(face, (snakes[ind].snake[0].x * size, snakes[ind].snake[0].y * size))
                for i in range(1, snakes[ind].tail):
                    win.blit(body, (snakes[ind].snake[i].x * size, snakes[ind].snake[i].y * size))
                win.blit(bush, (snakes[ind].fruct.pos.x * size, snakes[ind].fruct.pos.y * size))
                # Generation
                score_label = STAT_FONT.render("Generations: " + str(gen - 1), 1, (128, 128, 128))
                win.blit(score_label, (10, 10))
                # Current Score
                score_label = STAT_FONT.render("Score: " + str(snakes[ind].score), 1, (128, 128, 128))
                win.blit(score_label, (10, 50))
                # Max score
                score_label = STAT_FONT.render("Highscore: " + str(max_score), 1, (128, 128, 128))
                win.blit(score_label, (10, 90))
                pygame.display.update()
            else:
                draw = False
        except:
            pass
        pygame.display.update()


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 45)  # The number of generatations the functions will run
    print(winner)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    #run(config_path)
    replay_genome(config_path)
    # main()
