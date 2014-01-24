def enum(**enums):
    return type('Enum', (), enums)

r_type = enum(
  post = 'POST',
  get = 'GET',
  put = 'PUT',
  delete = 'DELETE',
  patch = 'PATCH'
  )

status_code = enum(
    success = 200,
    internal_error = 500,
    auth_failed = 401,
    invalid_field = 400,
    service_unavailable = 503
    )

status_group = enum(
    fail = [status_code.auth_failed,
            status_code.invalid_field],
    success = [status_code.success],
    retryable = [status_code.internal_error,
                status_code.service_unavailable]
    )

