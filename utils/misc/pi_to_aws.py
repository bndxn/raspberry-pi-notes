# Takes code from here https://medium.com/comsystoreply/a-step-by-step-guide-to-predictive-analytics-on-aws-generating-sensor-data-with-a-raspberry-pi-c84cf28b1b4b

# pip3 install boto3
"""
humidity_sensor.py
"""
import adafruit_dht
import board
import boto3
import datetime
import time

"""Initialize the sensor. Set correct board pin
"""
sensor = adafruit_dht.DHT11(board.D2)
AWS_S3_BUCKET = "bucket name"
AWS_S3_KEY_PREFIX = "/path/to/raw/sensor/data"

"""Initialize the AWS S3 service client. You need to set up authentication credentials for your AWS account before
using Boto3. You can use the `aws configure` command to configure the credentials file, or manually create it (the default location is ~/.aws/credentials)
"""
s3 = boto3.resource("s3")


class Reading:
    def __init__(self, temperature=None, temperature_f=None, humidity=None):
        self.timestamp = datetime.datetime.now().isoformat(timespec="milliseconds")
        self.temperature = temperature
        self.temperature_f = temperature_f
        self.humidity = humidity

    def to_csv(self):
        """CSV representation of the object
        Column order:
         - timestamp
         - temperature (Celsius)
         - temperature (Fahrenheit)
         - humidity
        """
        return (
            f"{self.timestamp},{self.temperature},{self.temperature_f},{self.humidity}"
        )


def get_reading() -> Reading:
    """Returns current readings from the sensor. Sensor DHT11 has sampling rate of 1 Hz, so calling this method more
    than once per second will result in the same readings
    """
    try:
        temperature = sensor.temperature
        temperature_f = temperature * (9 / 5) + 32
        humidity = sensor.humidity
        print(
            f"Temperature: {temperature:.1f} C ({temperature_f:.1f} F). Humidity: {humidity}%"
        )
        return Reading(temperature, temperature_f, humidity)

    except RuntimeError as error:
        print(error.args[0])
        return Reading()
    except Exception as error:
        sensor.exit()
        raise error


def upload_data(readings: list[Reading]):
    """Forms a CSV file and uploads it to AWS"""
    body = "\n".join(map(Reading.to_csv, readings))
    filename = f"readings-{datetime.datetime.now().isoformat(timespec='seconds')}.csv"
    s3object = s3.Object(AWS_S3_BUCKET, AWS_S3_KEY_PREFIX + filename)
    s3object.put(Body=body)
    print(f"File uploaded: {filename}")


if __name__ == "__main__":
    readings = list[Reading]()
    while True:
        reading = get_reading()
        readings.append(reading)
        if len(readings) >= 60:
            """Approximately every minute readings are uploaded to AWS S3"""
            upload_data(readings)
            readings.clear()
        time.sleep(1.0)
