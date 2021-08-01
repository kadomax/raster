import pygame
import math_load
import time
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



def render_object(screen , vertices , indices):
    screen_space_vertices = []
    for vertex in vertices:
        projected_vertex = math_load.project(vertex , SCREEN_HEIGHT / SCREEN_WIDTH)
        screen_space_vertex = math_load.toscreen(projected_vertex , SCREEN_WIDTH , SCREEN_HEIGHT)
        screen_space_vertices.append(screen_space_vertex)
    
    
    for tri_index in indices:
        v1 = vertices[tri_index[0]]
        v2 = vertices[tri_index[1]]
        v3 = vertices[tri_index[2]]

        vcam = math_load.vec3(0 , 0 , math_load.CAM_DISTANCE)
        normal_towards_camera = (((v3-v1) % (v2-v1)) ^ (v1 - vcam))
        light = math_load.calc_light(v1 , v2 , v3)
        if normal_towards_camera > 0 and light > 0:
            points = [
                (screen_space_vertices[tri_index[0]].x , screen_space_vertices[tri_index[0]].y),
                (screen_space_vertices[tri_index[1]].x , screen_space_vertices[tri_index[1]].y),
                (screen_space_vertices[tri_index[2]].x , screen_space_vertices[tri_index[2]].y)
            ]
            pygame.draw.polygon(screen , (round(50*light) , round(200*light) , round(100*light)) , points)




def transform_object(vertices):
    for i in range(len(vertices)):
        vertices[i] = math_load.rotate(2 , vertices[i] , 'y')
        vertices[i] = math_load.rotate(1 , vertices[i] , 'x')
    return vertices


def main():
    path = "models/" + "sphere.obj"
    verts = math_load.load_verts(path)
    indices = math_load.load_indices(path)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # # rotate light
        # math_load.LIGHT_VECTOR = math_load.rotate(2 , math_load.LIGHT_VECTOR , 'y')

        screen.fill((0 , 0 , 0))

        verts = transform_object(verts)
        render_object(screen , verts , indices)

        pygame.display.update()
        time.sleep(1/60)
    pygame.quit()

main()

