
import Foundation
import AVFoundation
import AudioKit
import Alamofire


class VoiceViewModel : NSObject, ObservableObject , AVAudioPlayerDelegate{
    
    var audioRecorder : AVAudioRecorder!
    var audioPlayer : AVAudioPlayer!
    
    var indexOfPlayer = 0
    var curFileName = URL(string: "")
    
    @Published var isRecording : Bool = false
    
    @Published var recordingsList = [Recording]()
    
    @Published var countSec = 0
    @Published var timerCount : Timer?
    @Published var blinkingCount : Timer?
    @Published var timer : String = "0:00"
    @Published var toggleColor : Bool = false

    @Published var whisperText : String = ""
    @Published var loading : Bool = false
    @Published var tags : [Tag] = []
    
    // AI SHIT
    var playingURL : URL?
    
    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
       
        for i in 0..<recordingsList.count {
            if recordingsList[i].fileURL == playingURL {
                recordingsList[i].isPlaying = false
            }
        }
    }
    
  
    
    func startRecording() {
        let recordingSession = AVAudioSession.sharedInstance()
        do {
            try recordingSession.setCategory(.playAndRecord, mode: .default)
            try recordingSession.setActive(true)
        } catch {
            print("Cannot setup the Recording")
        }
        
        let path = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        curFileName = path.appendingPathComponent("rec-\(Date().toString(dateFormat: "dd-MM-YY_HH-mm-ss")).m4a")

        let settings = [
            AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
            AVSampleRateKey: 12000,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
        ]
        
        
        do {
            audioRecorder = try AVAudioRecorder(url: curFileName!, settings: settings)
            audioRecorder.prepareToRecord()
            audioRecorder.record()
            isRecording = true
            
            timerCount = Timer.scheduledTimer(withTimeInterval: 1, repeats: true, block: { (value) in
                self.countSec += 1
                self.timer = self.covertSecToMinAndHour(seconds: self.countSec)
            })
            blinkColor()
        } catch {
            print("Failed to Setup the Recording")
        }
    }
    
    
    func stopRecording(){
        print("stop index: \(indexOfPlayer)")
        audioRecorder.stop()
        
        self.loading = true
        
        isRecording = false
        
        self.countSec = 0
        self.timer = self.covertSecToMinAndHour(seconds: self.countSec)
        
        timerCount!.invalidate()
        blinkingCount!.invalidate()
        
        
        struct DecodableType: Decodable {
            let message: String
            let tags: String
            let tag_dates: String
        }
        
        let dateFormatter = DateFormatter()

        
//        AF.request("http://127.0.0.1:8000/text/target").responseString { response in
//            if response.value != nil {
//                print("Response String: \(response.value!)")
//            }
//        }
        
        AF.upload(multipartFormData: { multipartFormData in
            multipartFormData.append(self.curFileName!, withName: "file")
        }, to: "https://dump-ydop2zskta-wl.a.run.app/transcribe")
            .responseDecodable(of: DecodableType.self) { response in
                debugPrint(response)
                if response.value != nil {
                    self.whisperText = response.value?.message ?? ""
                    
                    if response.value?.tags != nil {
                        if response.value?.tag_dates == nil {
                            print("BAABBB")
                            return
                        }
                        let dates = response.value!.tag_dates.split(separator: ",")
                        let tags = response.value!.tags.split(separator: ",")
                        
                        if dates.count != tags.count {
                            print("MISMATCH COUNT")
                            print(dates)
                            print(tags)
                            return
                        }
                        
                        for i in 0...tags.count {
                            let tagDates = dates[i].split(separator: ";")
                            var outDates: [Date] = []
                            for j in 0...tagDates.count {
                                outDates.append(dateFormatter.date(from: String(tagDates[j]))!)
                            }
                            self.tags.append(
                                Tag(value: String(tags[i]), clicked: false, dates: outDates)
                            )
                        }
                    }
                    self.loading = false
                }
            }
              
    }
    
    
    func fetchAllRecording(){
        
        let path = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let directoryContents = try! FileManager.default.contentsOfDirectory(at: path, includingPropertiesForKeys: nil)

        for i in directoryContents {
            recordingsList.append(Recording(fileURL : i, createdAt:getFileDate(for: i), isPlaying: false))
        }
        
        recordingsList.sort(by: { $0.createdAt.compare($1.createdAt) == .orderedDescending})
        
    }
    
    
    func startPlaying(url : URL) {
        
        playingURL = url
        
        let playSession = AVAudioSession.sharedInstance()
        
        do {
            try playSession.overrideOutputAudioPort(AVAudioSession.PortOverride.speaker)
        } catch {
            print("Playing failed in Device")
        }
        
        do {
            audioPlayer = try AVAudioPlayer(contentsOf: url)
            audioPlayer.delegate = self
            audioPlayer.prepareToPlay()
            audioPlayer.play()
            
            for i in 0..<recordingsList.count {
                if recordingsList[i].fileURL == url {
                    recordingsList[i].isPlaying = true
                }
            }
            
        } catch {
            print("Playing Failed")
        }
        
        
    }
    
    func stopPlaying(url : URL) {
        
        audioPlayer.stop()
        
        for i in 0..<recordingsList.count {
            if recordingsList[i].fileURL == url {
                recordingsList[i].isPlaying = false
            }
        }
    }
    
 
    func deleteRecording(url : URL) {
        
        do {
            try FileManager.default.removeItem(at: url)
        } catch {
            print("Can't delete")
        }
        
        for i in 0..<recordingsList.count {
            
            if recordingsList[i].fileURL == url {
                if recordingsList[i].isPlaying == true{
                    stopPlaying(url: recordingsList[i].fileURL)
                }
                recordingsList.remove(at: i)
                
                break
            }
        }
    }
    
    func blinkColor() {
        
        blinkingCount = Timer.scheduledTimer(withTimeInterval: 0.3, repeats: true, block: { (value) in
            self.toggleColor.toggle()
        })
        
    }
    
    
    func getFileDate(for file: URL) -> Date {
        if let attributes = try? FileManager.default.attributesOfItem(atPath: file.path) as [FileAttributeKey: Any],
            let creationDate = attributes[FileAttributeKey.creationDate] as? Date {
            return creationDate
        } else {
            return Date()
        }
    }
    
    
    
}
