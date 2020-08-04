#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from time import sleep

pygame.init()
screen = pygame.display.set_mode((800, 600))

pygame.draw.rect(screen, (225, 0, 23), pygame.Rect(42, 15, 40, 32))
pygame.display.flip()

sleep(10)