import pygame
import pytmx
import time
import customtkinter


def startGame():
    global score
    score = 0
    # Initialisieren von Pygame
    pygame.init()

    # music abspielen
    #pygame.mixer.music.load('BoulderDashThemeSong.mp3')

    # Konstanten für das Spiel
    WIDTH, HEIGHT = 800, 608
    GRID_SIZE = 32  # Größe eines Spielfeldes in Pixel
    BLACK = (0, 0, 0)  # Schwarze Hintergrundfarbe

    # Erstellen des Spielfensters
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boulder Dash")

    # Tilemap laden
    tm = pytmx.load_pygame("boulderdashMap.tmx")

    # Klasse für Tiles erstellen
    class Tile:
        def __init__(self, image, x, y):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

    # Erde-Tile
    earth_image = pygame.image.load("dirt.png")
    earth_tile = Tile(earth_image, 0, 0)

    # Mauer-Tile
    wall_image = pygame.image.load("wall.png")
    wall_tile = Tile(wall_image, 0, 0)

    # Rock-Tile
    rock_image = pygame.image.load("rock.png")
    rock_tile = Tile(rock_image, 0, 0)

    # Spieler
    player_image = pygame.image.load("player.png")
    player_rect = player_image.get_rect()
    player_rect.topleft = (128, 64)  # Hier setzen wir die Startposition oben links

    # Zeitmessung für die Bewegung
    last_move_time = time.time()
    move_cooldown = 0.2  # Bewegung alle 100 ms

    # Funktion zum Entfernen der Erde aus der Tilemap
    def remove_earth(tilemap, x, y, layer_index):
        tilemap.layers[layer_index].data[y][x] = 0

    # Spiel-Loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Zeit für die Bewegung abgelaufen
        if time.time() - last_move_time >= move_cooldown:
            # Bewegung des Spielers mit W, A, S, D
            keys = pygame.key.get_pressed()
            new_player_rect = player_rect.copy()  # Hier wird new_player_rect definiert
            if keys[pygame.K_a]:
                new_player_rect.x -= GRID_SIZE
            if keys[pygame.K_d]:
                new_player_rect.x += GRID_SIZE
            if keys[pygame.K_w]:
                new_player_rect.y -= GRID_SIZE
            if keys[pygame.K_s]:
                new_player_rect.y += GRID_SIZE

            # Kollision mit Mauern überprüfen
            collision = False
            for layer in tm.layers:
                if collision:
                    break
                if layer.name == "walls":
                    for x, y, tile_image in layer.tiles():
                        tile_rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                        if new_player_rect.colliderect(tile_rect):
                            collision = True
                            break
                elif layer.name == "rock":
                    for x, y, tile_image in layer.tiles():
                        tile_rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                        if new_player_rect.colliderect(tile_rect):
                            collision = True
                            break

            if not collision:
                # Überprüfen, ob der Spieler auf Erde steht
                player_tile_x = int(new_player_rect.x / GRID_SIZE)
                player_tile_y = int(new_player_rect.y / GRID_SIZE)
                earth_layer_index = None

                for i, layer in enumerate(tm.layers):
                    if layer.name == "earth":
                        earth_layer_index = i
                        break

                if earth_layer_index is not None:
                    earth_gid = tm.get_tile_gid(player_tile_x, player_tile_y, earth_layer_index)

                    # Überprüfen, ob der Spieler auf Erde steht und entfernen
                    if earth_gid != 0:
                        remove_earth(tm, player_tile_x, player_tile_y, earth_layer_index)

                player_rect = new_player_rect
                last_move_time = time.time()

        # Hintergrund löschen und Spieler zeichnen
        screen.fill(BLACK)  # Hintergrund auf Schwarz setzen

        # Tilemap rendern
        for layer in tm.layers:
            for x, y, image in layer.tiles():
                tile = Tile(image, x * GRID_SIZE, y * GRID_SIZE)
                screen.blit(tile.image, tile.rect)

        screen.blit(player_image, player_rect)
        pygame.display.flip()

    # Pygame beenden
    pygame.quit()

#def scoreUP():
#    score = score + 1
#    scoreBox.insert("0.0", "Punktestand: " + str(score))

#def scoreDown():
#    score = score - 1
#    scoreBox.insert("0.0", "Punktestand: " + str(score))

favicon = "BD-logo.ico"

app = customtkinter.CTk()
app.title("BoulderDash Launcher")
app.geometry("400x350")
customtkinter.set_appearance_mode("dark")
app.iconbitmap(favicon)

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)
app.grid_columnconfigure(3, weight=1)
app.grid_columnconfigure(4, weight=1)

app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_rowconfigure(3, weight=1)

button = customtkinter.CTkButton(app, text="Start Game", command=startGame)
button.grid(row=2, column=2, padx=20, pady=20)

scoreBox = customtkinter.CTkTextbox(app)
scoreBox.insert("0.0", "Drücke auf Start Game um das Spiel zu starten!") #"Punktestand: 0") # + str(score))
scoreBox.grid(row=1, column=2, padx=20, pady=20)


#scoreup = customtkinter.CTkButton(app, text="Score up", command=scoreUP)
#scoreup.grid(row=1, column=3, padx=20, pady=20)

#scoredown = customtkinter.CTkButton(app, text="Score down", command=scoreDown)
#scoredown.grid(row=1, column=1, padx=20, pady=20)

app.mainloop()