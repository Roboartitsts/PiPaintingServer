import abb
import time
import code

rob = abb.ABBRunner(2530,2530)
rob.connectToSerial("/dev/ttyUSB0")
print(rob.sendCanvasInfo())
time.sleep(3.5)
# rob.decidePaint("A")
scale = 2530



# rob.sendCoordB(0,0)
# time.sleep(3)
# rob.sendCoordB(2500,2500)
time.sleep(3.5)
p = [[],[],[]]
p[0] = [0,0]
p[1] = [1*scale,0]
p[2] = [1*scale,1*scale]

# rob.sendCoordQ(p[0][0], p[0][1], p[1][0], p[1][1], p[2][0],p[2][1])
# time.sleep(2)
rob.moveToSafe()
time.sleep(2)
rob.mixPaint(0)
time.sleep(2)
rob.moveToSafe()
# rob.moveUpsideDown()

# rob.followCurve()


code.interact(local=locals())
rob.abort()




  # if(left < 8){
  #   tempx = roby - int(round(sin((theta + 90)*convert)));
  #   tempy = robx + int(round(cos((theta + 90)*convert)));
  #   Serial.print(tempx);
  #   Serial.print(tempy);
  #   Serial.print("\n");
  # }
  # if(back< 8){
  #   tempx = roby - int(round(sin((theta + 180)*convert)));
  #   tempy = robx + int(round(cos((theta + 180)*convert)));
  #       Serial.print(tempx);
  #   Serial.print(tempy);
  #   Serial.print("\n");
  # }
  # if(right < 8){
  #   tempx = roby - int(round(sin((theta + 270)*convert)));
  #   tempy = robx + int(round(cos((theta + 270)*convert)));
  #       Serial.print(tempx);
  #   Serial.print(tempy);
  #   Serial.print("\n");
  # }
