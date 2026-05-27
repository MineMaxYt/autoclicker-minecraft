import java.awt.*;
import java.awt.event.*;

public class MinecraftAutoClicker {
    public static void main(String[] args) throws Exception {
        Robot robot = new Robot();
        while (true) {
            robot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
            robot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
            Thread.sleep(100); // 0.1 сек
        }
    }
}
