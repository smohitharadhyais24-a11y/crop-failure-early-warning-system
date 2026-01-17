"""
Initialize all models for the CFEWS system
Run this script to train yield predictor and crop recommender models
"""

if __name__ == '__main__':
    print("=" * 60)
    print("INITIALIZING CROP FAILURE EARLY WARNING SYSTEM MODELS")
    print("=" * 60)
    
    # Train main crop failure model
    print("\n[1/3] Training Crop Failure Prediction Model...")
    from backend.model.train import train_crop_failure_model
    train_crop_failure_model()
    
    # Train yield prediction model
    print("\n[2/3] Training Yield Prediction Model...")
    from backend.model.yield_predictor import train_yield_model
    train_yield_model()
    
    # Train crop recommender
    print("\n[3/3] Training Crop Recommendation Model...")
    from backend.model.crop_recommender import train_crop_recommender
    train_crop_recommender()
    
    print("\n" + "=" * 60)
    print("✅ ALL MODELS INITIALIZED SUCCESSFULLY!")
    print("=" * 60)
    print("\nYou can now start the Flask backend:")
    print("  python -m backend.app")
