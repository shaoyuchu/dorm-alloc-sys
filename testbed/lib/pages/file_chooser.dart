import 'package:file_chooser/file_chooser.dart';
import 'package:path_provider/path_provider.dart';

/// Possible file chooser operation types.
enum _FileChooserType { save, open }

/// Returns display text reflecting the result of a file chooser operation.
String _resultTextForFileChooserOperation(
    _FileChooserType type, FileChooserResult result) {
  if (result.canceled) {
    return '${type == _FileChooserType.open ? 'Open' : 'Save'} cancelled';
  }
  final typeString = type == _FileChooserType.open ? 'opening' : 'saving';
  return 'Selected for $typeString: ${result.paths.join('\n')}';
}