from config.supabase_config import supabase

def upload_to_supabase(file, filename="output.png", format="png"):
    try:
        upload_res = supabase.storage.from_('projects').upload(filename, file, file_options={"content-type": f"image/{format}", "upsert": "true"})

        public_url = supabase.storage.from_('projects').get_public_url(upload_res.path)
        
        return {"status": "SUCCESS", "result_url": public_url, "result_path": upload_res.path }
    except Exception as uploadErr:
        print(f"Couldn't upload the result image to storage: {str(uploadErr)}")
        return {"status": "FAILED", "error_code": "UPLOAD_ERROR"}




