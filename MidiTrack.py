import xml.etree.ElementTree as ET


class MidiTrack:
    def __init__(self, tree = None):

        self.tree = tree
        self.init()

    def init(self):
        if (self.tree == None):
            self.tree = ET.parse("midi_track.xml").getroot()

            # for rank in root.iter('rank'):
            #     new_rank = int(rank.text) + 1
            #     rank.text = str(new_rank)
            #     rank.set('updated', 'yes')
            #
            #


if __name__ == "__main__":
    track = MidiTrack()

