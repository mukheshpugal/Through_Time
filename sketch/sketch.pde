ArrayList<Agent> agents = new ArrayList<Agent>();
int AGENT_NUMBER = 0;

void setup() { 
  size(303, 303);
  strokeWeight(2);
  agents.add(new Agent(color(255, 0, 0), 0, 0));
  agents.add(new Agent(color(0, 255, 0), 0, 0));
  agents.add(new Agent(color(0, 0, 255), 0, 0));
}

void draw() {
  background(255);
  stroke(200);
  translate(1, 1);
  for (int i = 0; i < 11; i++) {
    line(30 * i, 0, 30 * i, height);
    line(0, 30 * i, width, 30 * i);
  }
  fill(0);
  ellipse(285, 285, 15, 15);
  for (Agent agent : agents) {
    agent.show();
  }
}

void keyPressed() {
  if (keyCode == UP) agents.get(AGENT_NUMBER).move(0);
  if (keyCode == RIGHT) agents.get(AGENT_NUMBER).move(1);
  if (keyCode == DOWN) agents.get(AGENT_NUMBER).move(2);
  if (keyCode == LEFT) agents.get(AGENT_NUMBER).move(3);
  if (key == 114) {AGENT_NUMBER--; if (AGENT_NUMBER < 0) AGENT_NUMBER = agents.size() - 1;} 
  if (key == 116) {AGENT_NUMBER++; if (AGENT_NUMBER > agents.size() - 1) AGENT_NUMBER = 0;}
  if (key == 115) {saveFrame("../assets/#####.png"); println("Frame saved");}
}
