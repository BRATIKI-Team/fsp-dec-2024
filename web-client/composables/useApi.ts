import useEvents from '~/composables/useEvents';
import useHelpers from '~/composables/useHelpers';
import type { IEvent } from '~/types/dtos/event';
import type { ISearchRequest, ISearchResponse } from '~/types/dtos/search';

export default () => {
  const events_api = useEvents();
  const helpers_api = useHelpers();

  const events_search = (request: ISearchRequest) =>
    $fetch<ISearchResponse<IEvent>>(helpers_api.REQUEST_URL('/events/search'), {
      method: 'POST',
      body: request,
      headers: helpers_api.AUTH_HEADERS(),
    }).then(response => ({
      ...response,
      items: response.items.map(item => events_api.map_after_request(item)),
    }));

  return {
    events: {
      search: events_search,
    },
  };
};
