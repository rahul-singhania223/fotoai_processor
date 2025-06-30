from models.BiRefNet.main import BiRefNetModel
from models.Real_ESRGAN.main import RealESRGANModel
from models.Zero_DCE.main import DCENetModel
from lib.utils import upload_to_supabase


if __name__ == "__main__":
   processor = DCENetModel()
   processor.process("https://images.pexels.com/photos/3819969/pexels-photo-3819969.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2")