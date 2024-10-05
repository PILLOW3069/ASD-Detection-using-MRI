from Model import asd_detector, cp_callback
from Data_Feeder import train_generator
asd_detector.fit(train_generator,
                     callbacks=[cp_callback],
                     steps_per_epoch=len(train_generator),
                     epochs=500)

asd_detector.save('ALLOUT_ASD_predictor_v1.keras')