import pygame

def main():
    print("Program Closed.")

pygame.init()
scr = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe_UI", 16)

# start values
h, s, l = 0, 100, 50 
brush = (0, 0, 0)
drawing = False
b_size = 10
last_pos = None  # Added for smooth lines
reset_btn = pygame.Rect(10, 350, 140, 40)

# 1. IMPORTANT: Fill white ONCE before the loop starts
scr.fill((255, 255, 255))

def get_clr(h_val, s_val, l_val):
    c = pygame.Color(0)
    c.hsla = (int(h_val) % 360, int(s_val), int(l_val), 100)
    return (c.r, c.g, c.b)

run = True
while run:
    # 2. UI DRAWING (Sidebar and Button)
    pygame.draw.rect(scr, (220, 220, 220), (0, 0, 160, 600)) # Gray Sidebar
    pygame.draw.rect(scr, brush, (40, 20, 80, 80))          # Brush Color Box
    
    # Text Stats
    stats = [f"H (Hue): {int(h)}", f"S (Sat): {int(s)}%", f"L (Light): {int(l)}%", f"Size: {b_size}px"]
    for i, txt in enumerate(stats):
        scr.blit(font.render(txt, True, (0,0,0)), (10, 120 + (i * 20)))

    # Instructions
    inst = ["K: ResetToBlack", "Spacebar: ClrCanvas", "Arrows: BrushSize"]
    for i, txt in enumerate(inst):
        scr.blit(font.render(txt, True, (60,60,60)), (10, 210 + (i * 22)))

    # Reset Button
    pygame.draw.rect(scr, (180, 180, 180), reset_btn) 
    pygame.draw.rect(scr, (0, 0, 0), reset_btn, 2)
    scr.blit(font.render("RESET ALL", True, (0, 0, 0)), (reset_btn.x + 35, reset_btn.y + 10))

    # 3. SINGLE EVENT LOOP
    for e in pygame.event.get():
        if e.type == pygame.QUIT: 
            run = False
        
        if e.type == pygame.MOUSEWHEEL:
            b_size = max(1, b_size + e.y * 2)

        if e.type == pygame.MOUSEBUTTONDOWN:
            if reset_btn.collidepoint(e.pos):
                # Clear canvas area
                pygame.draw.rect(scr, (255, 255, 255), (160, 0, 640, 600))
                h, s, l = 0, 100, 50 
            elif e.pos[0] > 160: 
                drawing = True
                
        if e.type == pygame.MOUSEBUTTONUP: 
            drawing = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP: b_size += 5
            if e.key == pygame.K_DOWN: b_size = max(1, b_size - 5)
            if e.key == pygame.K_SPACE:
                pygame.draw.rect(scr, (255, 255, 255), (160, 0, 640, 600))

    # 4. HSL LOGIC (Hold keys to change)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_h]: h += 2
    if keys[pygame.K_s]:
        if keys[pygame.K_LSHIFT]: s = max(0, s - 1)
        else: s = min(100, s + 1)
    if keys[pygame.K_l]:
        if keys[pygame.K_LSHIFT]: l = max(0, l - 1)
        else: l = min(100, l + 1)
    if keys[pygame.K_k]: s, l = 0, 0

    brush = get_clr(h, s, l)

    # 5. SMOOTH LINE DRAWING
    m_pos = pygame.mouse.get_pos()
    if drawing and m_pos[0] > 160:
        if last_pos:
            pygame.draw.line(scr, brush, last_pos, m_pos, b_size * 2)
            pygame.draw.circle(scr, brush, m_pos, b_size)
        last_pos = m_pos
    else:
        last_pos = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

if __name__=="__main__":
    main()
#Push/PullTEST