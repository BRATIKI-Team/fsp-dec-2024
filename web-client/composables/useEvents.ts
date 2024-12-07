import type { IEvent, IEventDetail } from '~/types/dtos/event';

export default () => {
  const map_after_request = (item: IEvent) => ({
    ...item,
    start_date: new Date(item.start_date),
    end_date: new Date(item.end_date),
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
