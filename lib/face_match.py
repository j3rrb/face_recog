from numpy import ndarray
from deepface.DeepFace import verify


class FaceMatch:
    def match(img: ndarray, target: ndarray) -> bool:
        output = verify(img, target)

        return output["verified"]
