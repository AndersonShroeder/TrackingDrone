def face_mesh(self, img):
    results = self.faceMesh.process(img)
    x, y = 0, 0
    landmark_locations = []
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            #draw facemesh
            self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpec, self.drawSpec)

            #loop through face landmarks to get actual data
            for lm in faceLms.landmark:
                ih, iw, ic = img.shape
                x, y = int(lm.x * iw), int(lm.y *ih) #multiply shape by normalized values (lm.x, lm.y) to get pixels
                landmark_locations.append([x,y])
    
    if self.emotion_detection:
        pass

    return img
