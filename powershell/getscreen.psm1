Function Get-Screen
{
    [void][Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
    $size = [Windows.Forms.SystemInformation]::VirtualScreen
    $bitmap = new-object Drawing.Bitmap $size.width, $size.height
    $graphics = [Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($size.location,[Drawing.Point]::Empty, $size.size)
    $graphics.Dispose()
    $bitmap.Save($args[0])
    $bitmap.Dispose()
}
