from a8t_tools.bus.producer import TaskProducer
from dependency_injector import containers, providers
from passlib.context import CryptContext

from app.domain.users.auth.commands import (
    TokenCreateCommand,
    TokenRefreshCommand,
    UserAuthenticateCommand,
)
from app.domain.users.auth.queries import (
    CurrentUserQuery,
    CurrentUserTokenPayloadQuery,
    CurrentUserTokenQuery,
    TokenPayloadQuery,
)
from app.domain.users.management.commands import UserManagementCreateCommand, UserManagementPartialUpdateCommand
from app.domain.users.management.queries import (
    UserManagementListQuery,
    UserManagementRetrieveQuery,
)
from app.domain.users.auth.repositories import TokenRepository
from app.domain.users.core.commands import (
    UserActivateCommand,
    UserCreateCommand,
    UserPartialUpdateCommand, UpdatePasswordRequestCommand,
    UpdatePasswordConfirmCommand,
)
from app.domain.users.core.queries import (
    UserListQuery,
    UserRetrieveByUsernameQuery,
    UserRetrieveQuery, UserRetrieveByEmailQuery, UserRetrieveByCodeQuery,
)
from app.domain.users.registration.hi import Generate_Password, First_Registration
from app.domain.users.core.repositories import UserRepository, \
    UpdatePasswordRepository, EmailRpository
from app.domain.users.permissions.queries import UserPermissionListQuery
from app.domain.users.permissions.services import UserPermissionService
from app.domain.users.registration.commands import UserRegisterCommand, UserEmailVerificationRequestCommand, \
    UserEmailVerificationConfirmCommand
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.security.hashing import PasswordHashService
from a8t_tools.security.tokens import JwtHmacService, JwtRsaService, token_ctx_var


class UserContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    task_producer = providers.Dependency(instance_of=TaskProducer)

    secret_key = providers.Dependency(instance_of=str)

    private_key = providers.Dependency(instance_of=str)

    public_key = providers.Dependency(instance_of=str)

    pwd_context = providers.Dependency(instance_of=CryptContext)

    access_expiration_time = providers.Dependency(instance_of=int)

    refresh_expiration_time = providers.Dependency(instance_of=int)

    user_repository = providers.Factory(
        UserRepository,
        transaction=transaction,
    )

    user_retrieve_query = providers.Factory(
        UserRetrieveQuery,
        user_repository=user_repository,
    )

    repository_update_password = providers.Factory(
        UpdatePasswordRepository,
        transaction=transaction,
    )

    repository_email_verification = providers.Factory(
        EmailRpository,
        transaction=transaction,
    )

    user_list_query = providers.Factory(
        UserListQuery,
        user_repository=user_repository,
    )

    retrieve_query = providers.Factory(
        UserRetrieveQuery,
        user_repository=user_repository,
    )

    retrieve_by_email_query = providers.Factory(
        UserRetrieveByEmailQuery,
        user_repository=user_repository,
    )

    retrieve_by_username_query = providers.Factory(
        UserRetrieveByUsernameQuery,
        repository=user_repository,
    )

    create_command = providers.Factory(
        UserCreateCommand,
        user_repository=user_repository,
        task_producer=task_producer,
    )

    activate_command = providers.Factory(
        UserActivateCommand,
        repository=user_repository,
    )

    generate_password = providers.Factory(
        Generate_Password,
    )

    first_registration = providers.Factory(
        First_Registration,
    )

    password_hash_service = providers.Factory(
        PasswordHashService,
        pwd_context=pwd_context,
    )

    jwt_rsa_service = providers.Factory(
        JwtRsaService,
        private_key=private_key,
        public_key=public_key,
        access_expiration_time=access_expiration_time,
        refresh_expiration_time=refresh_expiration_time,
    )

    jwt_hmac_service = providers.Factory(
        JwtHmacService,
        secret_key=secret_key,
        access_expiration_time=access_expiration_time,
        refresh_expiration_time=refresh_expiration_time,
    )

    partial_update_command = providers.Factory(
        UserPartialUpdateCommand,
        user_repository=user_repository,
    )

    token_ctx_var_object = providers.Object(token_ctx_var)

    current_user_token_query = providers.Factory(
        CurrentUserTokenQuery,
        token_ctx_var=token_ctx_var_object,
    )

    permission_list_query = providers.Factory(
        UserPermissionListQuery,
        query=retrieve_query,
    )

    register_command = providers.Factory(
        UserRegisterCommand,
        create_command=create_command,
        password_hash_service=password_hash_service,
    )

    email_verification_request_command = providers.Factory(
        UserEmailVerificationRequestCommand,
        repository=repository_email_verification,
    )

    email_verification_confirm_command = providers.Factory(
        UserEmailVerificationConfirmCommand,
        repository=repository_email_verification,
    )

    update_password_request_command = providers.Factory(
        UpdatePasswordRequestCommand,
        user_retrieve_by_email_query=retrieve_by_email_query,
        repository=repository_update_password,
    )

    get_userID_by_code = providers.Factory(
        UserRetrieveByCodeQuery,
        update_password_repository=repository_update_password,
        user_repository=user_repository
    )

    update_password_confirm_command = providers.Factory(
        UpdatePasswordConfirmCommand,
        user_retrieve_by_email_query=retrieve_by_email_query,
        repository=repository_update_password,
        user_partial_update_command=partial_update_command,
        user_retrieve_by_code_query=get_userID_by_code,
        password_hash_service=password_hash_service,
    )

    get_user_by_username = providers.Factory(
        UserRetrieveByUsernameQuery,
        repository=user_repository,
    )

    get_user_by_email = providers.Factory(
        UserRetrieveByEmailQuery,
        user_repository=user_repository,
    )

    token_repository = providers.Factory(TokenRepository, transaction=transaction)

    token_create_command = providers.Factory(
        TokenCreateCommand,
        jwt_service=jwt_rsa_service,
        repository=token_repository,
    )

    token_payload_query = providers.Factory(
        TokenPayloadQuery,
        jwt_service=jwt_rsa_service,
    )

    current_user_token_payload_query = providers.Factory(
        CurrentUserTokenPayloadQuery,
        token_query=current_user_token_query,
        token_payload_query=token_payload_query,
    )

    permission_service = providers.Factory(
        UserPermissionService,
        query=permission_list_query,
        current_user_token_payload_query=current_user_token_payload_query,
    )

    current_user_query = providers.Factory(
        CurrentUserQuery,
        token_query=current_user_token_payload_query,
        user_query=retrieve_query,
    )

    authenticate_command = providers.Factory(
        UserAuthenticateCommand,
        get_user_by_email=get_user_by_email,
        password_hash_service=password_hash_service,
        command=token_create_command,
    )

    refresh_token_command = providers.Factory(
        TokenRefreshCommand,
        repository=token_repository,
        query=token_payload_query,
        command=token_create_command,
        user_query=retrieve_query,
    )

    management_list_query = providers.Factory(
        UserManagementListQuery,
        permission_service=permission_service,
        query=user_list_query,
    )

    management_retrieve_query = providers.Factory(
        UserManagementRetrieveQuery,
        permission_service=permission_service,
        query=retrieve_query,
    )

    management_create_command = providers.Factory(
        UserManagementCreateCommand,
        permission_service=permission_service,
        command=register_command,
    )

    management_update_command = providers.Factory(
        UserManagementPartialUpdateCommand,
        permission_service=permission_service,
        command=partial_update_command,
    )
