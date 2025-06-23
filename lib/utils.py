from config.supabase import supabase

def upload_to_supabase(file):
    try:
        upload_res = supabase.storage.from_('uploads').upload("output.png", file, file_options={"content-type": "image/png", "upsert": "true"})

        public_url = supabase.storage.from_('uploads').get_public_url(upload_res.path)
        
        return {"status": "SUCCESS", "result_url": public_url }
    except Exception as uploadErr:
        print(f"Couldn't upload the result image to storage: {str(uploadErr)}")
        return {"status": "FAILED", "error_code": "UPLOAD_ERROR"}
