from rest_framework.exceptions import ValidationError

def validate_data(required_fields):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            data = request.data
            for field in required_fields:
                if field not in data:
                    raise ValidationError({'error': f'O campo {field} é obrigatório'})
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator