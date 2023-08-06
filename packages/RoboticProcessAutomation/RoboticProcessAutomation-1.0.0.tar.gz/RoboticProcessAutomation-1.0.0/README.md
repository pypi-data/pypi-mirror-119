# RoboticProcessAutomation
Some handy functions especially useful while building Robotic Process Automations with Python. <br />
Developed by *Bartosz Mazur*

## Table of contents

[Instalation](#instalation) <br />
[Simple usage](#simple-usage) <br />
[Documentation](#documentation) <br />
&ensp; [Image recognition based automations](#image-recognition-based-automations) <br />
&ensp; [Send keys based methods](#send-keys-based-methods) <br />
&ensp; [Environment prep](#environment-prep) <br />
&ensp; [Trace logs](#trace-logs) <br />
[License](#license)

## Instalation
```
pip install RoboticProcessAutomation
```

## Simple usage
```
import RoboticProcessAutomation as rpa

rpa.click_img('path/image1.png')
```

## Documentation

### Image recognition based automations
Based on well-known *PyAutoGui* lib. <br />
Ready to use functionalities, with a lot of additional parameters. <br />
Predefined with values, evaluated by me as good starting point for most cases.

* #### click_img()
  ```
  # IT WOULD TRY TO CLICK 3-TIMES, 100PX TO THE RIGHT FROM THE CENTER OF AN IMAGE_1:

  rpa.click_img('path/image1.png', off_x=100, target_retries=3)
  ```

  <strong>target</strong>: (str) - path to the img. <br />
  <strong>target_region</strong>: (tuple) - img region rectangle in [pixels] (x,y,width,height) <br />
  <strong>target_confidence</strong>: (float) - treshold for img recognition, 0.01 - ultra low 0.99 - high <br />
  <strong>target_retries</strong>: (int) - how many retries would be performed for click img <br />
  <strong>click_type</strong>: (str) - supported ones: single,double,right <br />
  <strong>off_x</strong>: (int) - x axis offset applied to click action, from center of the target img  <br />
  <strong>off_y</strong>: (int) - y axis offset applied to click action, from center of the target img  <br />
  <strong>mode</strong>: (str) <br />
  &nbsp; F -> return False  <br />
  &nbsp; E -> return Exception /default/ <br />
  <strong>wait_before_retry</strong>: (int) - how long it would wait until each retry. <br />
  <strong>click_before_retry</strong>: (tuple) - (x,y) to focus before retry <br />

* #### wait_img_appear()
* #### wait_img_dissapear()
  ```
  # IT WOULD WAIT UNTIL IMAGE_1 WOULD APPEAR ON THE SCREEN WITHIN (100,100,400,500) RECTANGLE
  # IT WOULD RETURN FALSE IF AFTER TIMEOUT, IMAGE_1 IS STILL NOT VISIBLE
  
  rpa.wait_img_appear('path/image1.png', target_region=(100,100,400,500), mode="F")
  
  # IT WOULD WAIT FOR APPROXIMATELY 30SEK UNTIL IMAGE_1 WOULD DISAPPEAR FROM THE SCREEN
  
  rpa.wait_img_disappear('path/image1.png', timeout=30)
  ```
  <strong>target</strong>: (str) - path to the img. <br />
  <strong>target_region</strong>: (tuple) - img region rectangle in [pixels] (x,y,width,height) <br />
  <strong>target_confidence</strong>: (float) - treshold for img recognition, 0.01 - ultra low 0.99 - high <br />
  <strong>timeout</strong>: (int) - how long it would wait for apperance [seconds]  <br />
  <strong>mode</strong>: (str) <br />
  &nbsp;  F -> return False <br />
  &nbsp;  E -> return Exception /default/ <br />
  
* #### click_img_2()
  Use-case example for this function might be click on MENU and wait/check if SUBMENU has appeared.

  ```
  # IT WOULD WAIT UNTIL IMAGE_2 WILL BE VISIBLE AFTER IMAGE_1 WAS CLICKED.
  # IT WOULD WAIT APPROXIMATELY 2SEK BEFORE CHECK IF IMAGE_2 IS ALREADY VISIBLE

  rpa.click_img_2('path/image1.png', click_type='double', check='path/image2.png', check_wait_before=2)
  ```

  <strong>target</strong>: (str) - path to the img.<br />
  <strong>target_region</strong>: (tuple) - img region rectangle in [pixels] (x,y,width,height)<br />
  <strong>target_confidence</strong>: (float) - treshold for img recognition, 0.01 - ultra low 0.99 - high<br />
  <strong>target_retries</strong>: (int) - how many retries would be performed for click img<br />
  <strong>click_type</strong>: (str) - supported ones: single,double,right<br />
  <strong>off_x</strong>: (int) - x axis offset applied to click action, from center of the target img <br />
  <strong>off_y</strong>: (int) - y axis offset applied to click action, from center of the target img <br />
  <strong>mode</strong>: (str)<br />
  &nbsp;   F -> return False <br />
  &nbsp;   E -> return Exception /default/<br />
  <strong>wait_before_retry</strong>: (int) - how long it would wait until each retry.<br />
  <strong>click_before_retry</strong>: (tuple) - (x,y) to focus before retry<br />
  <strong>check</strong>: (str) - path to img it would test for (dis)apperance<br />
  <strong>check_mode</strong>: (str)<br />
  &nbsp;  A - apperance<br />
  &nbsp;  D - disapperance<br />
  <strong>check_region</strong>: (tuple) - img region rectangle in [pixels] (x,y,width,height)<br />
  <strong>check_wait_before</strong>: (float) - how long it would wait until test<br />
  <strong>check_retries</strong>: (int) - how many test retries would be performed each loop run<br />
  <strong>check_timeout</strong>: (int) - to be passed into wait_img_a/d func <br />
  <strong>check_confidence</strong>: (float) - to be passed into wait_img_a/d func <br />

### Send keys based methods

* #### wait_write_press()

  ```
  wait_write_press(2, "text", "Enter")
  ```

  <strong>delay</strong>: (int) - delay time in [seconds]<br />
  <strong>text</strong>: (str) - text to be written<br />
  <strong>hotkey</strong>: (str) - hotkey to be pressed<br />

* #### wait_press()

  ```
  wait_press(2, "Enter")
  ```

  <strong>delay</strong>: (int) - delay time in [seconds]<br />
  <strong>hotkey</strong>: (str) - hotkey to be pressed<br />

* #### wait_write()

  ```
  wait_write(2, "text")
  ```

  <strong>delay</strong>: (int) - delay time in [seconds]<br />
  <strong>text</strong>: (str) - text to be written<br />


### Environment prep

* #### clear_folder()

  ```
  clear_folder('path_to_the_folder')
  ```
  
  <strong>path</strong>: (str) - path to the folder to be cleared
  
* #### kill_process()

  ```
  kill_process(['process.exe'])
  ```
  
  <strong>processes</strong>: (list[str]) - e.g. [process_1_name, (...), process_n_name] 

### Trace logs

* trace_log() </br>
  This function is to log robots trace info in the file. <br />
  And takes screenshots while status E,B,F would occur. <br />
  *Some statuses has been already suggested by me ;)* <br />



  ```
  trace_log('S')
  ```


  <strong>status</strong>: (str) <br />
  &nbsp; [S] start/stop <br />
  &nbsp; [T] trace <br />
  &nbsp; [E] error <br />
  &nbsp; [B] business error <br />
  &nbsp; [W] warning <br />
  &nbsp; [F] fatal <br />
  <strong>msg</strong>: (str) - custom error message, left blank will produce /traceback/ msg <br />
  <strong>path_log</strong>: (str) - path where log file would be saved <br />
  <strong>path_img</strong>: (str) - path where screenshot would be saved <br />

## License
MIT