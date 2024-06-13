import maya.cmds as cmds
import os


class TextureRetarget:
    """Class for checking and setting texture locations.

    This class identifies missing texture files and checks a user defined area
    for the missing textures.

    I've split up the checking and retargetting into seperate methods in the
    event a GUI was ever used. This way, the texture paths and nodes they came
    from can be displayed on screen and the retarget_from_folder could be used
    in a button and a lineedit widget
    """

    def __init__(self) -> None:
        self.files_to_retarget: dict = {}

        self.check_textures()

    def check_textures(self):
        """Checks if textures are missing.

        Gets a list of all file nodes in the scene. Checks if it can find the
        file on disk. If not it will store it in a dict of [node, str].
        where the node is the file node and the str is the path
        """
        files = cmds.ls(type="file")

        for _file in files:
            filePath = cmds.getAttr(_file + ".fileTextureName")

            if filePath == "":
                continue

            if not os.path.exists(filePath):
                print(f"Flagging for retargeting - {filePath}")
                self.files_to_retarget[_file] = filePath

    def retarget_from_folder(self, target_folder: str):
        """Takes the file node and points it to a new user defined location.

        Uses the file node and the original file path to get the file name and
        checks the new location for the file, if it exists it will set the
        attribute on the node to it.
        """
        for file_node in self.files_to_retarget:
            target_found: bool = False
            original_filepath = self.files_to_retarget[file_node]
            file_name = os.path.basename(original_filepath)

            for root, dirs, files in os.walk(target_folder):
                for file in files:
                    if file == file_name:
                        new_path = os.path.join(root, file)
                        print(f"Retargeting Texture - FROM - "
                              f"{original_filepath} | TO - {new_path} "
                        )

                        cmds.setAttr(
                            file_node + ".fileTextureName",
                            new_path,
                            type="string"
                        )
                        self.files_to_retarget[file_node] = new_path
                        target_found = True

                    if target_found:
                        break
                if target_found:
                    break

            if not target_found:
                print(f"Failed to retarget - {file_name}")