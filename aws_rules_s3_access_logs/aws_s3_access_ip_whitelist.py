from ipaddress import ip_network
# IP addresses (in CIDR notation) indicating approved IP ranges for accessing S3 buckets
IP_WHITELIST = {
    ip_network('10.0.0.0/8'),
}


def rule(event):
    # Only evaluate if the remoteIP field is present
    if 'remoteIP' not in event:
        return False

    cidr_ip = ip_network(event['remoteIP'])
    return not any(
        cidr_ip.subnet_of(approved_ip_range)
        for approved_ip_range in IP_WHITELIST)


def dedup(event):
    return event.get('bucket')


def title(event):
    return 'Non-Approved Access to S3 Bucket {}'.format(event.get('bucket'))
