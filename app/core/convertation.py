from datetime import datetime


class DataConverter:
    def get_header(self):
        raise NotImplementedError()

    def convert_item(self, item: dict):
        raise NotImplementedError()


class V1Header:
    ID = 'id'
    NAME = 'Name'
    DATE = 'Date'
    START_TIME = 'Start Time'
    END_TIME = 'End Time'
    LOCATION = 'Location'
    IS_LOCKED = 'Is Locked? (yes/no)'
    MAX_CAPACITY = 'Max.Capacity'
    SPEAKERS = 'Speakers (id:status;id:status)'
    OWNERS = 'Owners (emails)'
    ATTENDEES = 'Attendees (emails)'
    RESOURCES = 'Resources (ids)'
    FILTER_SESSION_TYPE = 'filter: Session Type'
    FIELD_LEARNING_OBJECTIVES = 'field: Learning Objectives'
    FIELD_TRACKS = 'field: Track(s)'
    FIELD_CHAIRS = 'field: Chair(s)'
    FIELD_CME_CREDITS = 'field: CE/MOC Credit(s)'
    FIELD_PRESENTATIONS = 'field: Presentations(s)'

    @staticmethod
    def as_list() -> list:
        return [
            V1Header.ID,
            V1Header.NAME,
            V1Header.DATE,
            V1Header.START_TIME,
            V1Header.END_TIME,
            V1Header.LOCATION,
            V1Header.IS_LOCKED,
            V1Header.MAX_CAPACITY,
            V1Header.SPEAKERS,
            V1Header.OWNERS,
            V1Header.ATTENDEES,
            V1Header.RESOURCES,
            V1Header.FILTER_SESSION_TYPE,
            V1Header.FIELD_LEARNING_OBJECTIVES,
            V1Header.FIELD_TRACKS,
            V1Header.FIELD_CHAIRS,
            V1Header.FIELD_CME_CREDITS,
            V1Header.FIELD_PRESENTATIONS,
        ]


class V1DataConverter(DataConverter):
    def get_header(self) -> list:
        return V1Header.as_list()

    def convert_item(self, item: dict) -> dict:
        return {
            V1Header.ID: item['SessionLocationId'],
            V1Header.NAME: item['SessionTitle'],
            V1Header.DATE: self._format_as_date(item['SessionDT']),
            V1Header.START_TIME: self._format_as_time(
                item['SessionStartTime']),
            V1Header.END_TIME: self._format_as_time(item['SessionEndTime']),
            V1Header.LOCATION: item['ActualRoom'],
            V1Header.IS_LOCKED: '',
            V1Header.MAX_CAPACITY: '',
            V1Header.SPEAKERS: '',
            V1Header.OWNERS: '',
            V1Header.ATTENDEES: '',
            V1Header.RESOURCES: '',
            V1Header.FILTER_SESSION_TYPE: item['SessionTypeName'],
            V1Header.FIELD_LEARNING_OBJECTIVES: item['Description'],
            V1Header.FIELD_TRACKS: item['Tracks'],
            V1Header.FIELD_CHAIRS: ', '.join(item['Chairs']),
            V1Header.FIELD_CME_CREDITS: item['CMECredits'],
            V1Header.FIELD_PRESENTATIONS: self._stringify_presentations(
                item['SessionParticipations']
            ),
        }

    def _stringify_presentations(self, presentations: list) -> str:
        def stringify_presentation(presentation: dict):
            return (
                '{topic}\n'
                '{start_time} - {end_time}\n'
                '{chair} - {role}\n'
                '{institution}\n'
            ).format(
                topic=presentation['IndividualTopic'],
                start_time=self._format_as_time(presentation['IndvSTime']),
                end_time=self._format_as_time(presentation['IndvETime']),
                chair=presentation['DisplayNameWithDesignation'],
                role=presentation['Role'],
                institution=presentation['Institution'],
            )

        return '\n'.join(map(stringify_presentation, presentations))

    def _format_as_date(self, string: str) -> str:
        if string is None:  # it seems some dates are not defined
            return ''

        dt = self._parse_datetime(string)
        return dt.strftime('%Y-%m-%d')

    def _format_as_time(self, string: str) -> str:
        if string is None:  # it seems some dates are not defined
            return ''

        dt = self._parse_datetime(string)
        return dt.strftime('%I:%M%p')

    def _parse_datetime(self, value) -> datetime:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
