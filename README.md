## Sentry <> Github Team Sync Webhook Handler

### What is this webhook handler for?

The goal is to use this webhook handler to receive requests from Github when there are changes to any GH teams. The handler currently supports the following operations/callbacks:

- New Team created
- Team deleted
- Member added to an existing team
- Member removed from an existing team

### How to use this webhook handler?

This is a flask server that needs to be hosted in a fully qualified domain name (FQDN), which is resolvable on the internet.

In order to run this server succesfully, you will need to add the following environment variables:

<b>GH_TOKEN</b>

The handler uses a GH authentication token which can be obtained from any of the ways listed [here](https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api?apiVersion=2022-11-28) (This was tested with a fine-grained personal token) <b>[Settings] -> [Developer Settings] -> Personal Access Tokens -> Fine-grained tokens </b> (No permissions required for fine-grained personal tokens)

<b>SENTRY_TOKEN<b>

The handler uses a Sentry Auth Token to call the [Team API endpoints](https://docs.sentry.io/api/teams/)
You can create a token by following this [guide](https://docs.sentry.io/organization/integrations/integration-platform/internal-integration/#auth-tokens), with Team Admin and Member Read&Write permissions

<b>SENTRY_ORG_SLUG<b>

Your Sentry org slug. Found under <b>[Settings] -> [Organization Settings] -> [Organization Slug]</b>. Used to build the API url endpoints.

<b>GH_WEBHOOK_TOKEN<b>

Your [Secret Token](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries#creating-a-secret-token) used to validate and authenticate requests coming from GH. Make sure that this value is the same as the one added to the Webhook Settings

### How to set up the webhook

1. Go to your GH organization settings
2. Create a new webhook under <b>[Code, planning and automation] -> [Webhooks]</b>
3. Add the payload URL to the domain where this server is hosted
4. Select `application/json` under Content type
5. Add the secret to the webhook (It has to be the same string as the one in your env variable)
6. Under `Which events would you like to trigger this webhook`, select:
	- Memberships
	- Teams
7. Save changes

After following the steps, the payload URL should get called once any of the events specified in the webhook is called.
