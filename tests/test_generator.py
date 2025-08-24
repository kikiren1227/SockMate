import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from core.generator.base import BaseParams, ImageReferenceParams, ImageGenerator, HFGenerator


class TestBaseParams:
    """Test BaseParams class and its create method"""
    
    def test_create_with_required_params(self):
        """Test creating BaseParams with only required parameters"""
        params = BaseParams.create("a red sock")
        
        assert params["prompt"] == "a red sock"
        assert params["width"] == 512  # default
        assert params["height"] == 512  # default
        assert params["negative_prompt"] is None
        assert params["guidance_scale"] is None
        assert params["seed"] is None
    
    def test_create_with_all_params(self):
        """Test creating BaseParams with all parameters"""
        params = BaseParams.create(
            prompt="a blue sock",
            width=768,
            height=768,
            negative_prompt="ugly, blurry",
            guidance_scale=7.5,
            seed=42
        )
        
        assert params["prompt"] == "a blue sock"
        assert params["width"] == 768
        assert params["height"] == 768
        assert params["negative_prompt"] == "ugly, blurry"
        assert params["guidance_scale"] == 7.5
        assert params["seed"] == 42
    
    def test_create_with_custom_dimensions(self):
        """Test creating BaseParams with custom width and height"""
        params = BaseParams.create("a green sock", width=1024, height=512)
        
        assert params["width"] == 1024
        assert params["height"] == 512
        assert params["prompt"] == "a green sock"
    
    def test_create_with_float_guidance_scale(self):
        """Test creating BaseParams with float guidance_scale"""
        params = BaseParams.create("a purple sock", guidance_scale=8.5)
        
        assert params["guidance_scale"] == 8.5
        assert isinstance(params["guidance_scale"], float)
    
    def test_create_with_int_guidance_scale(self):
        """Test creating BaseParams with int guidance_scale"""
        params = BaseParams.create("a yellow sock", guidance_scale=7)
        
        assert params["guidance_scale"] == 7
        assert isinstance(params["guidance_scale"], int)


class TestImageReferenceParams:
    """Test ImageReferenceParams class"""
    
    def test_inheritance_from_base_params(self):
        """Test that ImageReferenceParams inherits from BaseParams"""
        assert issubclass(ImageReferenceParams, BaseParams)
    
    def test_additional_fields(self):
        """Test that ImageReferenceParams has the additional fields"""
        # Check that the fields exist in the class
        assert "reference_image" in ImageReferenceParams.__annotations__
        assert "control_type" in ImageReferenceParams.__annotations__


class TestImageGenerator:
    """Test ImageGenerator abstract base class"""
    
    def test_is_abstract(self):
        """Test that ImageGenerator is abstract and cannot be instantiated"""
        with pytest.raises(TypeError):
            ImageGenerator()
    
    def test_has_abstract_generate_method(self):
        """Test that ImageGenerator has abstract generate method"""
        assert hasattr(ImageGenerator, 'generate')
        assert ImageGenerator.generate.__isabstractmethod__


class TestHFGenerator:
    """Test HFGenerator class"""
    
    def test_initialization(self):
        """Test HFGenerator initialization"""
        generator = HFGenerator("test_token", "https://test.url")
        
        assert generator._api_token == "test_token"
        assert generator._url == "https://test.url"
    
    def test_inheritance_from_image_generator(self):
        """Test that HFGenerator inherits from ImageGenerator"""
        assert issubclass(HFGenerator, ImageGenerator)
    
    @patch('requests.post')
    def test_generate_success(self, mock_post):
        """Test successful image generation"""
        # Mock successful response
        mock_response = Mock()
        mock_response.content = b"fake_image_data"
        mock_post.return_value = mock_response
        
        generator = HFGenerator("test_token", "https://test.url")
        params = BaseParams.create("a red sock", width=512, height=512)
        
        result = generator.generate(params)
        
        assert result == b"fake_image_data"
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        assert call_args[0][0] == "https://test.url"  # URL
        assert call_args[1]["headers"]["Authorization"] == "Bearer test_token"
        
        payload = call_args[1]["json"]
        assert payload["inputs"] == "a red sock"
        assert payload["parameters"]["width"] == "512"
        assert payload["parameters"]["height"] == "512"
    
    @patch('requests.post')
    def test_generate_with_http_error(self, mock_post):
        """Test handling of HTTP errors"""
        # Mock HTTP error
        mock_post.side_effect = requests.HTTPError("HTTP Error")
        
        generator = HFGenerator("test_token", "https://test.url")
        params = BaseParams.create("a red sock")
        
        # Should not raise exception, just print error
        result = generator.generate(params)
        
        assert result is None  # No return value on error
    
    @patch('requests.post')
    def test_generate_with_network_error(self, mock_post):
        """Test handling of network errors"""
        # Mock network error
        mock_post.side_effect = requests.ConnectionError("Connection Error")
        
        generator = HFGenerator("test_token", "https://test.url")
        params = BaseParams.create("a red sock")
        
        # Should not raise exception, just print error
        result = generator.generate(params)
        
        assert result is None  # No return value on error
    
    def test_generate_with_different_params(self):
        """Test generation with different parameter combinations"""
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.content = b"fake_image_data"
            mock_post.return_value = mock_response
            
            generator = HFGenerator("test_token", "https://test.url")
            
            # Test with different dimensions
            params = BaseParams.create("a large sock", width=1024, height=768)
            result = generator.generate(params)
            
            assert result == b"fake_image_data"
            
            # Verify payload has correct dimensions
            call_args = mock_post.call_args
            payload = call_args[1]["json"]
            assert payload["parameters"]["width"] == "1024"
            assert payload["parameters"]["height"] == "768"


class TestIntegration:
    """Integration tests for the generator system"""
    
    def test_full_workflow(self):
        """Test the complete workflow from params creation to generation"""
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.content = b"generated_sock_image"
            mock_post.return_value = mock_response
            
            # Create parameters
            params = BaseParams.create(
                prompt="a colorful striped sock",
                width=768,
                height=768,
                negative_prompt="ugly, plain",
                guidance_scale=7.5,
                seed=12345
            )
            
            # Create generator
            generator = HFGenerator("api_token_123", "https://api.huggingface.co/models/stabilityai/stable-diffusion-2-1")
            
            # Generate image
            result = generator.generate(params)
            
            # Verify result
            assert result == b"generated_sock_image"
            
            # Verify all parameters were used correctly
            call_args = mock_post.call_args
            payload = call_args[1]["json"]
            
            assert payload["inputs"] == "a colorful striped sock"
            assert payload["parameters"]["width"] == "768"
            assert payload["parameters"]["height"] == "768" 