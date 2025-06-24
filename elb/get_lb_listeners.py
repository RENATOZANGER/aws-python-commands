from config.aws_config import get_session


def get_lb_listeners(client, load_balancer_arn):
    """
    Get listeners of  Load Balancer by its ARN.
    """
    try:
        response = client.describe_listeners(LoadBalancerArn=load_balancer_arn)
        listeners = response.get('Listeners', [])
        
        if not listeners:
            print(f"No listeners found for Load Balancer {load_balancer_arn}.")
            return []
        for listener in listeners:
            print(f"Listener ARN: {listener['ListenerArn']}")
            print(f"Protocol: {listener['Protocol']}")
            print(f"Port: {listener['Port']}")
            print('-------------------------')
    except Exception as e:
        print(f"Error retrieving listeners for Load Balancer {load_balancer_arn}: {e}")

if __name__ == "__main__":
    elb_client = get_session().client('elbv2')
    lb_arn = "lb_arn"
    listeners = get_lb_listeners(elb_client, lb_arn)
