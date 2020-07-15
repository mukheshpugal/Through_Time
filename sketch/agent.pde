class Agent {
  color c;
  int x, y;
  Agent(color c, int x, int y){
    this.c = c;
    this.x = x;
    this.y = y;
  }

  void show() {
    noStroke();
    fill(c);
    rect(30*x + 5, 30*y + 5, 20, 20, 5); 
  }
  
  void move(int direction) {
    // 0 - Top
    // 1 - Right
    // 2 - Bottom
    // 3 - Left
    if (direction == 0) y--;
    else if (direction == 1) x++;
    else if (direction == 2) y++;
    else if (direction == 3) x--;
    if (y < 0) y = 0;
    else if (y > 9) y = 9;
    else if (x < 0) x = 0;
    else if (x > 9) x = 9;
  }
}
