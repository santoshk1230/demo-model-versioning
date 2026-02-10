import json
import logging
import copy
from datetime import datetime
import traceback

class LambdaLogger:
    def __init__(self, service_name="LambdaService", log_level=logging.INFO):
        """
        Initialize the logger with a service name and log level.
        
        Args:
            service_name (str): Name of the service for log context.
            log_level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        """
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(log_level)
        self.service_name = service_name

    def _sanitize_event(self, event):
        """
        Remove event['body']['input'] from the event to avoid logging sensitive data.
        
        Args:
            event (dict): The Lambda event object.
        
        Returns:
            dict: A sanitized copy of the event.
        """
        try:
            # Create a deep copy to avoid modifying complete event
            sanitized_event = copy.deepcopy(event)
            if isinstance(sanitized_event, dict) and 'body' in sanitized_event:
                
                if isinstance(sanitized_event['body'], str):
                    # If body is a JSON string, parse it, remove 'input', and re-serialize
                    try:
                        sanitized_event['body'] = json.loads(sanitized_event['body'])
                        # if isinstance(body_dict, dict) and 'input' in body_dict:
                        #     del body_dict['input']
                        #     sanitized_event['body'] = body_dict
                    except json.JSONDecodeError:
                        # If body is not valid JSON, leave it as is
                        pass
                if 'input' in sanitized_event['body']:
                    req_id = sanitized_event['body']['input']['requestId']
                    del sanitized_event['body']['input']
                    sanitized_event['body']['x-group-id'] = req_id
            return sanitized_event['body']
        except Exception as e:
            # Log error if sanitization fails, but don't fail the execution
            self.logger.error(f"Error sanitizing event: {str(e)}")
            return event

    def log_entry(self, event, response, context):
        """
        Log the incoming Lambda request, excluding event['body']['input'].
        
        Args:
            event (dict): The Lambda event object.
            context (object): The Lambda context object.
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service_name,
            "request_id": context.aws_request_id,
            "request": self._sanitize_event(event),
            "response": response
            
        }
        self.logger.info(json.dumps(log_entry))

    
    def log_error(self, error, context):
        """
        Log an error that occurred during Lambda execution.
        
        Args:
            error (Exception): The exception object.
            context (object): The Lambda context object.
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service_name,
            "request_id": context.aws_request_id,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "stack_trace": traceback.format_exc(),
            "log_type": "error"
        }
        self.logger.error(json.dumps(log_entry))