import type { IEvent, IEventDetail } from '~/types/dtos/event';

export default () => {
  const map_after_request = (item: IEvent) => ({
    ...item,
    datetime: new Date(item.datetime),
  });

  const map_detail_after_request = (item: IEventDetail) => ({
    ...item,
    event: map_after_request(item.event),
  });

  return {
    map_after_request,
    map_detail_after_request,
  };
};
