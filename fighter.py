import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, jump):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 4 #lil footnote: 0: atk 1, 1: atk 2, 2: dead , 3: boing, 4: idle, 5: mundur, 6: run 7: take hit
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        #make sure it's drawn on screen. assign rectangle.
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.boing = False
        self.atking = False
        self.attack_type = 0
        self.atk_cd = 0
        self.hit = False
        self.atk_sound = sound
        self.jump = jump
        self.alive = True
        self.health = 100

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            #enumerate is a tracker
         #extracting images from sheets.
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            
            animation_list.append(temp_img_list)
        return animation_list
        
    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        
        #start off with not running
        self.running = False
        self.attack_type = 0
        #keypresses
        key = pygame.key.get_pressed()

        
        if self.player == 1:
            if self.alive == True and self.atking == False and round_over == False:
                #moov
                if key[pygame.K_a]:
                        dx = -SPEED
                        self.running = True
                if key[pygame.K_d]:
                        dx = SPEED
                        self.running = True

                    #boing boing
                if key[pygame.K_w] and self.boing == False :
                        self.vel_y = -30
                        self.boing = True
                        self.jump.play()
                #can only whack after another whack
                    #whack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.atk(target)
                    #which atk type
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                            self.attack_type = 2
        #p2
        if self.player == 2:
            if self.alive == True and self.atking == False:
                    #moov
                if key[pygame.K_LEFT]:
                        dx = -SPEED
                        self.running = True
                if key[pygame.K_RIGHT]:
                        dx = SPEED
                        self.running = True

                    #boing boing
                if key[pygame.K_UP] and self.boing == False :
                        self.vel_y = -30
                        self.boing = True
                        self.jump.play()
                #can only whack after another whack
                    #whack
                if key[pygame.K_o] or key[pygame.K_p]:
                    self.atk(target)
                        #which atk type
                    if key[pygame.K_o]:
                        self.attack_type = 1
                    if key[pygame.K_p]:
                        self.attack_type = 2


        #apply physics
        self.vel_y += GRAVITY
        dy += self.vel_y

        #make sure players stick to screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left

        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        if self.rect.bottom + dy > screen_height - 70:
            self.vel_y = 0
            self.boing = False
            dy = screen_height - 70 - self.rect.bottom
        #facing each other?
        if target.rect.centerx > self.rect.centerx:
             self.flip = False
        else:
             self.flip = True

        #atk cd
        if self.atk_cd > 0:
            self.atk_cd -= 1   


        #updating positions
        self.rect.x += dx
        self.rect.y += dy

        #aneemationsss
    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(2)
        #check what action
        elif self.hit == True:
            self.update_action(7)#kena gebuk
        elif self.atking == True:
            if self.attack_type == 1:
                self.update_action(0)#regular move
            elif self.attack_type == 2:
                self.update_action(1)#special move  
        elif self.boing == True:
            self.update_action(3)#boing boing bakudan
        elif self.running == True:
            self.update_action(6)#run from reality bois
        else:
            if self.action != 4:  # Check if not already in idle state
                self.update_action(4)  # Return to idle


        anm_cd = 100
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last one
        if pygame.time.get_ticks() - self.update_time > anm_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #if anim finish
        if self.frame_index >= len(self.animation_list[self.action]):
            # if the player is wasted end the anim
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # Reset to idle after hit animation completes
                if self.action == 7:  # Check if in hit state
                    self.hit = False
                    self.update_action(4)  # Return to idle
            #if already attack:
                if self.action == 0 or self.action == 1:
                    self.atking = False
                    self.atk_cd = 10
            #check if dmg taken
                if self.action == 5:
                    self.hit = False
                    #if player is in the middle of an atk its stops.
                    self.atking = False
                    self.atk_cd = 10 
        max_frames = len(self.animation_list[self.action])
        if max_frames > 0:
            self.frame_index %= max_frames  # Ensure frame index stays within range

            

    def atk(self, target):
        if self.atk_cd == 0:
            self.atking = True
            self.atk_sound.play()
            atking_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * (1 if self.flip else 0)),self.rect.y, 4 * self.rect.width, self.rect.height)
            if atking_rect.colliderect(target.rect):
                target.health -=5
                target.hit = True
            #pygame.draw.rect(surface, (0,255,0), atking_rect)

    def update_action(self, new_action):
        #check if new action is diff 
        if new_action != self.action:
             self.action = new_action
    
        #update animation settings
             self.frame_index = 0
             self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
        