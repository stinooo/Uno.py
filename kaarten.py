import pygame

kaarten = {
    "B0": pygame.image.load("files/Blue_0.png"),
    "B1": pygame.image.load("files/Blue_1.png"),
    "B2": pygame.image.load("files/Blue_2.png"),
    "B3": pygame.image.load("files/Blue_3.png"),
    "B4": pygame.image.load("files/Blue_4.png"),
    "B5": pygame.image.load("files/Blue_5.png"),
    "B6": pygame.image.load("files/Blue_6.png"),
    "B7": pygame.image.load("files/Blue_7.png"),
    "B8": pygame.image.load("files/Blue_8.png"),
    "B9": pygame.image.load("files/Blue_9.png"),
    "BDR": pygame.image.load("files/Blue_Draw.png"),
    "BRE": pygame.image.load("files/Blue_Reverse.png"),
    "BSK": pygame.image.load("files/Blue_Skip.png"),
    "G0": pygame.image.load("files/Green_0.png"),
    "G1": pygame.image.load("files/Green_1.png"),
    "G2": pygame.image.load("files/Green_2.png"),
    "G3": pygame.image.load("files/Green_3.png"),
    "G4": pygame.image.load("files/Green_4.png"),
    "G5": pygame.image.load("files/Green_5.png"),
    "G6": pygame.image.load("files/Green_6.png"),
    "G7": pygame.image.load("files/Green_7.png"),
    "G8": pygame.image.load("files/Green_8.png"),
    "G9": pygame.image.load("files/Green_9.png"),
    "GDR": pygame.image.load("files/Green_Draw.png"),
    "GRE": pygame.image.load("files/Green_Reverse.png"),
    "GSK": pygame.image.load("files/Green_Skip.png"),
    "G0": pygame.image.load("files/Green_0.png"),
    "G1": pygame.image.load("files/Green_1.png"),
    "G2": pygame.image.load("files/Green_2.png"),
    "G3": pygame.image.load("files/Green_3.png"),
    "G4": pygame.image.load("files/Green_4.png"),
    "G5": pygame.image.load("files/Green_5.png"),
    "G6": pygame.image.load("files/Green_6.png"),
    "G7": pygame.image.load("files/Green_7.png"),
    "G8": pygame.image.load("files/Green_8.png"),
    "G9": pygame.image.load("files/Green_9.png"),
    "GDR": pygame.image.load("files/Green_Draw.png"),
    "GRE": pygame.image.load("files/Green_Reverse.png"),
    "GSK": pygame.image.load("files/Green_Skip.png"),
    "R0": pygame.image.load("files/Red_0.png"),
    "R1": pygame.image.load("files/Red_1.png"),
    "R2": pygame.image.load("files/Red_2.png"),
    "R3": pygame.image.load("files/Red_3.png"),
    "R4": pygame.image.load("files/Red_4.png"),
    "R5": pygame.image.load("files/Red_5.png"),
    "R6": pygame.image.load("files/Red_6.png"),
    "R7": pygame.image.load("files/Red_7.png"),
    "R8": pygame.image.load("files/Red_8.png"),
    "R9": pygame.image.load("files/Red_9.png"),
    "RDR": pygame.image.load("files/Red_Draw.png"),
    "RRE": pygame.image.load("files/Red_Reverse.png"),
    "RSK": pygame.image.load("files/Red_Skip.png"),
    "Y0": pygame.image.load("files/Yellow_0.png"),
    "Y1": pygame.image.load("files/Yellow_1.png"),
    "Y2": pygame.image.load("files/Yellow_2.png"),
    "Y3": pygame.image.load("files/Yellow_3.png"),
    "Y4": pygame.image.load("files/Yellow_4.png"),
    "Y5": pygame.image.load("files/Yellow_5.png"),
    "Y6": pygame.image.load("files/Yellow_6.png"),
    "Y7": pygame.image.load("files/Yellow_7.png"),
    "Y8": pygame.image.load("files/Yellow_8.png"),
    "Y9": pygame.image.load("files/Yellow_9.png"),
    "YDR": pygame.image.load("files/Yellow_Draw.png"),
    "YRE": pygame.image.load("files/Yellow_Reverse.png"),
    "YSK": pygame.image.load("files/Yellow_Skip.png"),
    "W": pygame.image.load("files/Wild.png"),
    "WD": pygame.image.load("files/Wild_Draw.png"),
}
achterkant= pygame.image.load("files/Deck.png")

class Kaart:
    def __init__(self, afbeelding, x, y, zichtbaar=True):
        self.afbeelding = afbeelding
        self.x = x
        self.y = y
        self.zichtbaar = zichtbaar

    def teken(self, scherm):
        if self.zichtbaar:
            scherm.blit(self.afbeelding, (self.x, self.y))
        else:
            scherm.blit(achterkant, (self.x, self.y))
            
gedeelde_kaarten = [ 
        Kaart(kaarten["R1"], 100, 100, zichtbaar=True),
        Kaart(kaarten["G2"], 150, 100, zichtbaar=True),
    ]